//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.List;

public class WilfulDefaultersList {
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");

//    public List<AmlExtractionResponse> read_WilfulDefaultersList(String path, String harvestingLink) {
//        List<AmlExtractionResponse> aml_extracts = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--lang=en");
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        try {
            driver.get("https://infogram.com/wilful-defaults-borrowers-names-1g9vp11kv1zgp4y");
            try {
                Thread.sleep(60000);
            }
            catch (Exception e) {

            }

            List<WebElement> entities = driver.findElements(By.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr"));
//            System.out.println(entities.size());

            for (int i = 1; i <= entities.size(); i++) {
                String bank = driver.findElement(By.xpath("/html[1]/body[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[1]/span[1]")).getText();
                String borrower = driver.findElement(By.xpath("/html[1]/body[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[2]")).getText();
                borrower = borrower.replaceAll("\\(PREV", "").trim();
                String directors = driver.findElement(By.xpath("/html[1]/body[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[3]/span[1]")).getText();
                String outstanding_amt = driver.findElement(By.xpath("/html[1]/body[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[4]")).getText();

//                AmlExtractionResponse aml_extract = new AmlExtractionResponse();
//                aml_extract.setCategory("Sanction");
//                aml_extract.setEntityType("Organisation");
//                aml_extract.setNationality("Indian");
//                aml_extract.setRiskLevel("International");
//                aml_extract.setFullName(borrower);
                System.out.println(borrower);
//                aml_extract.setSummary(borrower + " has an outstanding amount of " + outstanding_amt + " to the bank " + bank + ". ");
                String summary = borrower + " has an outstanding amount of " + outstanding_amt + " to the bank " + bank + ". ";
                if (!directors.equals("nil"))
//                    aml_extract.setSummary(aml_extract.getSummary() + "Names of directors of " + borrower + " are: " + directors);
                    System.out.println(summary + "Names of directors of " + borrower + " are: " + directors);
//                aml_extract.setCountry("India");

//                aml_extracts.add(aml_extract);



            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            driver.quit();
        }
//        return aml_extracts;
    }
}