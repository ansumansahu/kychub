//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SuspendedAndBlacklistedNGOs {
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");
//    public List<AmlExtractionResponse> read_SuspendedAndBlacklistedNGOs(String path, String harvestingLink) throws IOException {
//        List<AmlExtractionResponse> aml_extracts = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--lang=en");
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        try {

            driver.get("http://www.socialjustice.nic.in/UserView/index?mid=73590");
            List<WebElement> ngos = driver.findElements(By.xpath("/html[1]/body[1]/div[3]/section[1]/div[1]/div[2]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr/td[2]"));
//            System.out.println(ngos.size());
            for (int i = 2; i <= 122; i++) {
                String details = driver.findElement(By.xpath("/html[1]/body[1]/div[3]/section[1]/div[1]/div[2]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[2]")).getText();
                String name = details.split(", ")[0].trim();
                String address = details.substring(details.indexOf(",") + 2).trim();
                String summary = "Action taken by the Ministry: " + driver.findElement(By.xpath("/html[1]/body[1]/div[3]/section[1]/div[1]/div[2]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr[" + i + "]/td[3]")).getText();
                summary = summary.replaceAll("\n", " ");
                if (summary.contains("(size"))
                    summary = summary.substring(0, summary.indexOf("(size")).trim();

                summary = name + " falls under the Grants Suspended/Blacklisted NGOs list put forth by the Department of Social Justice and Empowerment. " + summary;

//                AmlExtractionResponse aml_extract = new AmlExtractionResponse();

//                aml_extract.setEntityType("Organisation");
//                aml_extract.setCategory("Sanction");
//                aml_extract.setRiskLevel("National");
//                aml_extract.setNationality("Indian");
//                aml_extract.setCountry("India");
//                aml_extract.setFullName(name);
                System.out.println(name);
//                aml_extract.setSummary(summary);
                System.out.println(summary);
//                aml_extract.setAddressLine1(address);
                System.out.println(address);

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