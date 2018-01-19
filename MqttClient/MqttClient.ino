#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>

//#define DEBUG

#define DATA_PIN     3

#define CMD_INIT_PANEL      1
#define CMD_CLEAR_PANEL     2
#define CMD_FILL_PANEL      3
#define CMD_PAINT_PANEL     4
#define CMD_SET_PIXEL       5
#define CMD_WRITE_RAW       6

#define CMD_SET_FRAME_NR  254
#define CMD_SHOW          255

uint16_t numberOfLeds; 

byte* leds;

char ssid[] = "FRITZ!Box 6360 Cable";
char password[] = "4249789363748310";
char mqtt_server[] = "nebuhr";

/**
char ssid[]        = "***"; // ssid of your accesspoint     
char password[]    = "***"; // password for your accesspoint 
char mqtt_server[] = "***"; // IP or hostname of your mqtt server
**/

byte mac[6];                                  // Buffer for storing the MAC Address.
uint16_t currentFrameNr;

WiFiClient* espClient;
PubSubClient* client;

void startWIFI(const char* ssid, const char* password) {
  delay(1000);
  #ifdef DEBUG
  Serial.println(ssid);
  #endif
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.persistent(false);
    WiFi.mode(WIFI_OFF);   // this is a temporary line, to be removed after SDK update to 1.5.4
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      #ifdef DEBUG
      Serial.print(".");
      #endif
    }
  }

  #ifdef DEBUG
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  #endif

  WiFi.macAddress(mac);
}

uint16_t bytesToWord(uint8_t high,uint8_t low) {
  uint16_t result = high; 
  result <<= 8;
  result |= low;
  return result;
}

boolean checkFrameConsistency(uint16_t frameNr) {
  if (frameNr == currentFrameNr) return true;
  if (frameNr > currentFrameNr) {
    FastLED.clear();
    currentFrameNr = frameNr;
    return true;
  }
  #ifdef DEBUG
  Serial.print("Wrong frame. Got ");
  Serial.print(frameNr);
  Serial.print(" expected at least ");
  Serial.println(currentFrameNr);
  #endif
  
  return false;
}

void callback(char* topic, byte* payload, unsigned int length) {
  #ifdef DEBUG
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.print("Length ");
  Serial.print(length);
  Serial.print(" Command ");
  Serial.println(payload[0]);
  #endif
  
  switch (payload[0]) {
    case CMD_INIT_PANEL:
      initPanel(payload, length);
      break;

    case CMD_SET_PIXEL:
      setPixel(payload, length);
      break;

    case CMD_SHOW:
      showPanel(payload, length);
      break;

    case CMD_WRITE_RAW:
      cmdWriteRaw(payload, length);
      break;

    case CMD_SET_FRAME_NR:
      cmdSetFrameNr(payload,length);
      break;
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client->connected()) {
    #ifdef DEBUG
    Serial.print("Attempting MQTT connection...");
    #endif
    // Create a random client ID
    String clientId = "LEDPANEL0001";
    // Attempt to connect
    if (client->connect(clientId.c_str())) {
      #ifdef DEBUG
      Serial.println("connected");
      #endif
      // Once connected, publish an announcement...
      client->publish("DEVICELOGON", "LEDPANEL0001");
      // ... and resubscribe
      client->subscribe("LEDPANEL0001");
    } else {
      #ifdef DEBUG
      Serial.print("failed, rc=");
      Serial.print(client->state());
      Serial.println(" try again in 5 seconds");
      #endif
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

/**
 * Sets the current frame number.
 * 
 * If the command byte is other than CMD_SET_FRAME_NR
 * the operation will be canceled.
 * If the length is not 3, the operation will be canceled.
 * 
 * Byte Position
 * =============
 * 0 : Command Byte. must be CMD_SET_FRAME_NR
 * 1 : HIGH byte of the frame number
 * 2 : LOW byte of the frame number
 * 
 */
void cmdSetFrameNr(byte* cmdbuffer, uint16_t length) {
  if (cmdbuffer[0] != CMD_SET_FRAME_NR) return;
  if (length != 3) return;
  currentFrameNr = bytesToWord(cmdbuffer[1], cmdbuffer[2]);
}

/**
 * Write some bytes directly to the led buffer. 
 * Currently no check for 'Index out of Bounds'
 * violation.
 * 
 * Byte Position
 * =============
 * 0 : Command Byte. must be CMD_WRITE_RAW
 * 1 : HIGH Byte of frame number
 * 2 : LOW Byte of frame number
 * 3 : HIGH Byte of starting index
 * 4 : LOW Byte of starting index
 * 5 : HIGH Byte of number of bytes to write 
 * 6 : LOW Byte of number of bytes to write
 * 7 : First byte to write. All following bytes
 *     will be copied directly to the ledbuffer.
 *     
 *     @since: 15.01.2018
 */
void cmdWriteRaw(byte* cmdbuffer, uint16_t length) {
  if (leds == NULL) return; 
  if (cmdbuffer[0] != CMD_WRITE_RAW) return;
  
  // Check if enough bytes are availabel to read the 
  // Parameters.
  //
  if (length < 7) return;

  uint16_t frameNumber = bytesToWord(cmdbuffer[1], cmdbuffer[2]);
  if (checkFrameConsistency(frameNumber)) {
    uint16_t startIndex = bytesToWord(cmdbuffer[3], cmdbuffer[4]);
    if (startIndex >= (numberOfLeds * 3)) return;
    uint16_t numBytes = bytesToWord(cmdbuffer[5], cmdbuffer[6]);
    if (startIndex+numBytes > (numberOfLeds * 3)) return; 
    memcpy(leds+startIndex,cmdbuffer+7,numBytes);
  }
}

/**
 * Initializes the "panel"
 * If the provided frame number is smaller than the curent frame number,
 * the operation will be canceled.
 * 
 * If the memory for the leds already has been allocated, the operation 
 * will be canceled.
 * 
 * If the first byte ist not CMD_SHOW, the operation will be canceled.
 * 
 * Byte Position
 * =============
 * 0 : Command Byte. must be CMD_SHOW
 * 1 : width of the panel. The number of leds per row.
 * 2 : height of the panel. The number of rows.
 * 3 : HIGH byte of the initial frame nr. .
 * 4 : LOW byte of the initial frame nr. 
 */
void initPanel(byte* cmdbuffer, uint16_t length) {
  if (cmdbuffer[0] != CMD_INIT_PANEL) return;
  if (leds != NULL) free(leds); 
  
  const byte width  = cmdbuffer[1];
  const byte height = cmdbuffer[2];
  
  currentFrameNr = bytesToWord(cmdbuffer[3],cmdbuffer[4]);
  
  numberOfLeds = width * height;
  
  leds = (byte*) malloc(numberOfLeds * 3);
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, numberOfLeds);
  memset8(leds,0,numberOfLeds * 3);
  FastLED.showColor(CRGB::Green);
}

/**
 * Updates the LEDs,
 * If the provided frame number is smaller than the curent frame number,
 * the operation will be canceled.
 * 
 * If length is not 3, operation will be canceled.
 * 
 * Byte Position
 * =============
 * 0 : Command Byte. must be CMD_SHOW
 * 1 : HIGH byte frame nr to be updated.
 * 2 : LOW byte frame nr to be updated. 
 */
void showPanel(byte* cmdbuffer, uint16_t length) {
  if (cmdbuffer[0] != CMD_SHOW) return;
  if (leds == NULL) return; 
  if (length != 3) return;
  
  const uint16_t fnr = bytesToWord(cmdbuffer[1],cmdbuffer[2]);
  #ifdef DEBUG
  Serial.print("Updating panel frame nr. ");
  Serial.print(fnr);
  Serial.print(". Current frame number is ");
  Serial.println(currentFrameNr);
  #endif
  // Are we updating the current frame?
  if (checkFrameConsistency(fnr)) {
    FastLED.show();
    currentFrameNr++;
  } 
}

/**
 * Set the r,g,b values at the given index.
 * 
 * There is no check if the index is to high. If no memory for
 * the leds has been allocated, the operation will be not be
 * performed.
 * If length is not 8, the operation will nor be performed.
 * 
 * The function does not check if the index is "well-aligned". 
 * Because every leds consumes three bytes, an align index is
 * dividable bei three. If, for example, the index is 2, then 
 * the blue value for led[0] and the red and green value for
 * led[1] will be set.
 * 
 * Byte Position
 * =============
 * 0 : Command Byte. must be CMD_SET_PIXEL
 * 1 : HIGH byte of the index.
 * 2 : LOW byte of the index. 
 * 3 : HIGH byte of target frame.
 * 4 : LOW byte of the target frame. 
 * 5 : red value for the pixel (if index is well aligned) 
 * 6 : green value for the pixel (if index is well aligned) 
 * 7 : blued value for the pixel (if index is well aligned) 
 */
void setPixel(byte* cmdBuffer, uint16_t length) {
  if (cmdBuffer[0] != CMD_SET_PIXEL) return;
  if (leds == NULL) return; 
  if (length != 8) return;
  
  uint16_t index = bytesToWord(cmdBuffer[1], cmdBuffer[2]);
  uint16_t fnr = bytesToWord(cmdBuffer[3],cmdBuffer[4]);
  
  #ifdef DEBUG
  Serial.print("Index: ");
  Serial.println(index);
  Serial.print("R: ");
  Serial.println(cmdBuffer[5]);
  Serial.print("G: ");
  Serial.println(cmdBuffer[6]);
  Serial.print("B: ");
  Serial.println(cmdBuffer[7]);
  #endif

  if (checkFrameConsistency(fnr)) {
    leds[index]   = cmdBuffer[5];
    leds[index+1] = cmdBuffer[6];
    leds[index+2] = cmdBuffer[7];
  } else {
    #ifdef DEBUG
    Serial.print(F("Wrong frame number. Got "));
    Serial.print(fnr);
    Serial.print(F(". Expected at least "));
    Serial.print(currentFrameNr);
    #endif     
  }
}

void setup() {
  Serial.begin(115200);
  delay(10);
  #ifdef DEBUG
  Serial.println("Off we go");
  #endif
  delay(3000);
  startWIFI(ssid, password);
  espClient = new WiFiClient();
  client = new PubSubClient(*espClient);
  client -> setServer(mqtt_server, 1883);
  client -> setCallback(callback);
  client -> subscribe("LEDPANEL0001");
}

void loop() {
  if (!client->connected()) {
    reconnect();
  }
  client->loop();
}
