//package com.kychub.aml.v1.manualdatasources.headless;
//
//import com.kychub.aml.v1.model.AmlExtractionResponse;
//import com.kychub.aml.v1.model.entity.Address;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;

public class CanadaEconomicMeasuresOnRussia {
    public static String camelCasing(String text) {
        text = text.trim();
        if (text.isEmpty()) {
            return text;
        } else {
            String[] array = text.split("\\s+");
            String name = "";
            for (int i = 0; i < array.length; i++) {
                String temp = "";
                temp = array[i].toUpperCase();
                name += temp.charAt(0) + temp.substring(1).toLowerCase() + " ";
            }
            return name.trim();
        }
    }

    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");

//    public List<AmlExtractionResponse> read_CanadaRussiaOrg(String path, String harvestingLink){
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        try {
            driver.get("http://www.canada.ca/en/global-affairs/news/2022/02/canada-imposes-additional-economic-measures-on-russia-in-response-to-russias-attack-on-ukraine.html");
            Thread.sleep(4000);

            String zz=driver.findElement(By.cssSelector(".cmp-text")).getText();
            try {
                zz=zz.substring(zz.indexOf("Entities:"),zz.indexOf("Special Economic Measures (Ukraine) Regulations\nIndividuals"));
            }catch (Exception e){}

            String []split=zz.split("\n");

            for(String z:split) {
                if (!z.contains(".")) continue;

                String name = "";
                String summary = "";

                try {
                    name = z.substring(z.indexOf("."));
                } catch (Exception e) {}

                name=name.replace(".","");
                name = camelCasing(name);

//                AmlExtractionResponse amlExtractionResponse= new AmlExtractionResponse();

                try {
                    name = z.substring(z.indexOf("."));
                } catch (Exception e) {}

                name=name.replace(".","");
                name = camelCasing(name);
                summary= "Canada imposes additional economic measures on Russia in response to Russia’s attack on Ukraine." +
                        "The Special Economic Measures (Russia) Regulations and the Special Economic Measures (Ukraine) Regulations impose dealings prohibitions on "+ name;


                if (!name.trim().isEmpty()) {
//                    amlExtractionResponse.setFullName(name.trim());
                    System.out.println(name);
                }

                if (!summary.trim().isEmpty()) {
//                    amlExtractionResponse.setSummary(summary.trim());
                }

//                amlExtractionResponses.add(amlExtractionResponse);
            }


        } catch (Exception e) {
        } finally {
            driver.quit();
        }
//        return amlExtractionResponses;
    }

}
