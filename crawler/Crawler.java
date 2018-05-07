import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.*;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.concurrent.TimeUnit;

import org.json.simple.JSONObject;

public class Crawler {
    private HashSet<String> productLinks = new HashSet<>();
    //private ArrayList<Product> products = new ArrayList<Product>();
    private int ID = 0;


    public Crawler() {

    }


    public void extractProductData(String categoryURL) {
        try {
            Document document = Jsoup.connect(categoryURL).get();
            Elements URLsOnPage = document.select("a[class='item_link']");

            for (Element page : URLsOnPage) {
                String URL = page.attr("abs:href");
                if (!productLinks.contains(URL)) {
                    productLinks.add(URL);
                    String title = page.attr("title");

                    //Open ad.
                    document = Jsoup.connect(URL).get();
                    String price = document.select("div[id='vi_price']").text();
                    String sellerName = document.select("a[id='login_to_reply_name']").text();
                    String modelYear = document.select("div[id='item_details']").select("strong").get(0).text();
                    String vehicleType = document.select("div[id='item_details']").select("strong").get(1).text();
                    String location = document.select("ul[id='seller-info']").select("span[class='area_label']").text();
                    String date = document.select("ul[id='seller-info']").select("time").attr("datetime");
                    String description = document.select("div[class='col-xs-12 body']").text();
                    String thumbnailURL = document.select("div[class*='carousel']").select("img").attr("src");

                    if (thumbnailURL.length() > 0 && URL.length() > 0 && title.length() > 0 && description.length() > 0
                            && location.length() > 0 && sellerName.length() > 0 && date.length() > 0 && price.length() > 0 &&
                            modelYear.length() == 4 && modelYear.chars().allMatch(Character::isDigit) && vehicleType.length() > 0) {
                        //products.add(new Product(URL, thumbnailURL, title, description, location, sellerName, date, price, modelYear, vehicleType));
                        writeDataToFile(URL, thumbnailURL, title, description, location, sellerName, date, price, modelYear, vehicleType);
                        ID++;
                    }

                    //System.out.println(URL + " " + thumbnailURL + " " + sellerName + " " + title + " " + price + " " + modelYear + " " + vehicleType + " " + location + " " + date + " " + description);
                }
            }
        }
        catch (IOException e) {
            System.err.println(categoryURL + " " + e.getMessage());
        }
    }


    ArrayList<String> getCategoryPages(String URLFormat) {
        ArrayList<String> categoryURLS = new ArrayList<String>();
        int maxNumberOfPages = 391;
        for (int pageNumber = 1; pageNumber <= maxNumberOfPages; pageNumber++) {
            categoryURLS.add(URLFormat + pageNumber);
        }

        return categoryURLS;
    }


    void writeDataToFile(String URL, String thumbnailURL, String title, String description, String location,
                         String sellerName, String date, String price, String modelYear, String vehicleType) {

        //Download the thumbnail image (name of image = ID of product).
        try(InputStream in = new URL(thumbnailURL).openStream()){
            Files.copy(in, Paths.get("thumbnails/" + ID + ".jpg"));
        }
        catch (Exception e) {
            System.out.println("Handled FileNotFound Exception");
            ID--;
            return;
        }

        JSONObject obj = new JSONObject();
        obj.put("id", ID);
        obj.put("url", URL);
        obj.put("title", title);
        obj.put("description", description);
        obj.put("location", location.replace("(","").replace(")",""));
        obj.put("sellerName", sellerName);
        obj.put("date", date);
        obj.put("price", Integer.parseInt(price.replace(" ","").replace("kr","")));
        obj.put("modelYear", Integer.parseInt(modelYear));
        obj.put("vehicleType", vehicleType);

        try {
            FileWriter file = new FileWriter("products/" + ID + ".json");
            file.write(obj.toJSONString());
            file.close();
        }
        catch (Exception e) {
            System.out.println(e);
        }
    }


    void crawlProductData() {
        String categoryURLFormat = "https://www.blocket.se/hela_sverige?q=&cg=1140&w=3&st=s&ps=&pe=&rs=&re=&c=&ca=11&l=0&md=th&o=";
        ArrayList<String> categoryURLS = getCategoryPages(categoryURLFormat);

        //Get all Product URLs from all category pages.
        int pageNumber = 1;
        for (String categoryURL : categoryURLS) {
            System.out.println("Crawling product data from page " + pageNumber + "...");
            extractProductData(categoryURL);
            pageNumber++;
            System.out.println("Waiting 15 seconds to prevent router from overheating...");
            try {
                TimeUnit.SECONDS.sleep(15);
            }
            catch (Exception e) {
                System.out.println(e);
            }
        }

        System.out.println("Number of products in category: " + ID);
    }


    public static void main(String[] args) {
        Crawler crawler = new Crawler();
        crawler.crawlProductData();
    }
}