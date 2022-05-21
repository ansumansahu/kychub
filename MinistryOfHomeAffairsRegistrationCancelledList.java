//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.List;

public class MinistryOfHomeAffairsRegistrationCancelledList {
    public static String camelCasing(String text){
        String[] array = text.split(" ");
        String name = "";
        for (int i=0;i<array.length; i++ ){
            String temp = "";
            temp = array[i].toUpperCase();
            name+= temp.charAt(0)+temp.substring(1).toLowerCase()+" ";
        }
        return name.trim();
    }
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");

//    public List<AmlExtractionResponse> read_MinistryOfHomeAffairsRegistrationCancelledList(String path, String harvestingLink) {

//        List<AmlExtractionResponse> responses = new ArrayList<>();

        ChromeOptions options = new ChromeOptions();
        options.addArguments("--lang=en");
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();
//        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);

        try {
            driver.get("https://fcraonline.nic.in/fc8_cancel_query.aspx");
            Thread.sleep(2000);

            driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/input")).click();
//            Thread.sleep(2000);
            Thread.sleep(4000);

            List<WebElement> tab = driver.findElements(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr"));
            for (int i = 20675; i <= tab.size(); i++) {
                String Category = "Organisation";
                String Name = "";
                String Regd_Number = "";
                String State = "";
                String Additional = "";
                String Cancellation_type = "";
                String Cancellation_year = "";
                String Country = "India";
                String Risk_level = "National";
                String Entity_type = "Watchlist";
                String Summary = "";

                try {
                    String name = driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr["+i+"]/td[3]")).getText();
                    Name = camelCasing(name);
                }catch (Exception ee){}


                try{
                    String regno = driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr["+i+"]/td[2]")).getText();
                    Regd_Number = regno;
                }catch (Exception ee){}


                try{
                    String state = driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr["+i+"]/td[4]")).getText();
                    State = state;
                }catch (Exception ee){}


                try{
                    String cancellation_type = driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr["+i+"]/td[5]")).getText();
                    Cancellation_type = cancellation_type;
                }catch (Exception ee){}


                try{
                    String year = driver.findElement(By.xpath("/html/body/form/section/div/div[2]/div/div/div/div/div/table/tbody/tr["+i+"]/td[6]")).getText();
                    Cancellation_year = year;
                }catch (Exception ee){}

                String summary = Name + "'s registration is cancelled by the ministry of home affairs of India under the reason "+Cancellation_type+ " in the year "+Cancellation_year;
                Summary = summary;

                if (Regd_Number.isEmpty() == false) {
                    if (Additional.isEmpty() == false) {
                        Additional += "; Registration Number: " + Regd_Number;
                    } else
                        Additional += "Registration Number: " + Regd_Number;
                }
                if (Cancellation_type.isEmpty() == false) {
                    if (Additional.isEmpty() == false) {
                        Additional += "; Cancellation type: " + Cancellation_type;
                    } else
                        Additional += "Cancellation type: " + Cancellation_type;
                }
                if (Cancellation_year.isEmpty() == false) {
                    if (Additional.isEmpty() == false) {
                        Additional += "; Cancellation Year: " + Cancellation_year;
                    } else
                        Additional += "Cancellation Year: " + Cancellation_year;
                }


                if (Name.trim().isEmpty() == false) {
//                    AmlExtractionResponse response = new AmlExtractionResponse();
//                    response.setFullName(Name);
                    System.out.println(Name);

                    if (State.trim().isEmpty() == false) {
//                        response.setState(State);
                        System.out.println(State);
                    }

                    if (Additional.trim().isEmpty() == false) {
//                        response.setAdditionalInfo(Additional);
                        System.out.println("add: "+Additional);
                    }
                    if (Name.trim().isEmpty() == false) {
//                        response.setSummary(Summary);
                        System.out.println(summary);
                    }
//                    if (Name.trim().isEmpty() == false) {
//                        response.setEntityType(Entity_type);
//                    }
//                    if (Name.trim().isEmpty() == false) {
//                        response.setCountry(Country);
//                    }
//                    if (Name.trim().isEmpty() == false) {
//                        response.setCategory(Category);
//                    }
//                    if (Name.trim().isEmpty() == false) {
//                        response.setRiskLevel(Risk_level);
//                    }

//                    responses.add(response);

                }
            }

        } catch (Exception e) {

        } finally {
            driver.quit();
        }

//        return responses;
    }
}