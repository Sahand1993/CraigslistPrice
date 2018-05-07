import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.io.FileReader;
import java.io.FileWriter;

public class JSONMerger {
    public static void main(String[] args) {
        try {
            FileWriter file = new FileWriter("motorcycles.json");
            JSONParser parser = new JSONParser();

            int numberOfMotorcycles = 18811;
            for (int i = 0; i < numberOfMotorcycles; i++) {
                JSONObject motorcycle = (JSONObject) parser.parse(new FileReader("products/" + i + ".json"));
                file.write("{\"index\":{\"_index\":\"simple\",\"_type\":\"motorcycle\"}}");
                file.write("\n");
                file.write(motorcycle.toJSONString());
                if (i < numberOfMotorcycles - 1) {
                    file.write("\n");
                }
            }

            file.close();
        }
        catch (Exception e) {
            System.out.println(e);
        }
    }
}