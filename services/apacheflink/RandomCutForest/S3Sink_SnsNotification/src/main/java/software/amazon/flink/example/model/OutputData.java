package software.amazon.flink.example.model;

public class OutputData {

    private String deviceId;
    private int timestamp;   // ISO8601
    private float value;
    private boolean isActive;
    private String eventId;

    private double score;       // ← 追加（必須）
    private int anomalyFlag = 0; // ← 追加（0/1）

    public OutputData() {}

    public OutputData(String deviceId, int timestamp, float value, boolean isActive, String eventId, double score) {
        this.deviceId = deviceId;
        this.timestamp = timestamp;
        this.value = value;
        this.isActive = isActive;
        this.eventId = eventId;
        this.score = score;
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

    public double getScore() { return score; }
    public void setScore(double score) { this.score = score; }

    public int getAnomalyFlag() { return anomalyFlag; }
    public void setAnomalyFlag(int anomalyFlag) { this.anomalyFlag = anomalyFlag; }

    /** JSON Lines 用: 1 行 = 1 レコード */
    public String toJsonString() {
        return String.format(
            "{\"device_id\":\"%s\",\"timestamp\":\"%d\",\"value\":%s,\"is_active\":%s,\"event_id\":\"%s\",\"score\":%s,\"anomaly_flag\":%d}",
            deviceId, String.valueOf(timestamp), Float.toString(value), Boolean.toString(isActive), eventId, Double.toString(score), anomalyFlag
        );
    }

    /** CSV 用: device_id,timestamp,value,event_id,score,anomaly_flag （ヘッダ別管理） */
    public String toCsvRow() {
        return String.join(",",
                safe(deviceId), 
                String.valueOf(timestamp),
                Float.toString(value),
                Boolean.toString(isActive),
                safe(eventId),
                Double.toString(score),
                Integer.toString(anomalyFlag)
        );
    }

    private String safe(String s) { return s == null ? "" : s.replace("\"","\"\""); }

    @Override
    public String toString() {
        return "OutputData{" +
                "device_id=" + deviceId +
                ", timestamp=" + timestamp +
                ", value=" + value +
                ", is_active=" + isActive +
                ", eventId=" + eventId +
                ", score=" + score +
                ", anomaly_flag=" + anomalyFlag +
                '}';
    }
}
