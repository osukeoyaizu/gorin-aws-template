package software.amazon.flink.example.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class InputData {

    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("timestamp")      // ISO8601 文字列
    private int timestamp;

    @JsonProperty("value")
    private float value;
    
    @JsonProperty("is_active")
    private boolean isActive;

    @JsonProperty("event_id")
    private String eventId;

    public InputData() {}

    public InputData(String deviceId, int timestamp, float value, boolean isActive, String eventId) {
        this.deviceId = deviceId;
        this.timestamp = timestamp;
        this.value = value;
        this.isActive = isActive;
        this.eventId = eventId;
    }

    public String getDeviceId() { return deviceId; }
    public void setDeviceId(String deviceId) { this.deviceId = deviceId; }

    public int getTimestamp() { return timestamp; }
    public void setTimestamp(int timestamp) { this.timestamp = timestamp; }

    public float getValue() { return value; }
    public void setValue(float value) { this.value = value; }

    public boolean getIsActive() { return isActive; }
    public void setIsActive(boolean isActive) { this.isActive = isActive; }

    public String getEventId() { return eventId; }
    public void setEventId(String eventId) { this.eventId = eventId; }

    @Override
    public String toString() {
        return "InputData{" +
                "device_id=" + deviceId +
                ", timestamp=" + timestamp +
                ", value=" + value +
                ", is_active=" + isActive +
                ", eventId=" + eventId +
                '}';
    }
}
