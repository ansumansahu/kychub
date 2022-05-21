//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class OFACSanctionsOnRussiaIndividuals2 {
    static String dOBTransformer(String dob){
        List<String> months = Arrays.asList("January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December");
        List<String> mon = Arrays.asList("01","02","03","04","05","06","07","08","09","10","11","12");

        for (int l=0;l<months.size();l++){
            if (dob.contains(months.get(l))){
                String mm = mon.get(l);
                String dd = dob.trim().split(" ")[1];
                dd = dd.replace(",", "");
                String yyyy = dob.trim().split(" ")[2];
                dob = dd+"/"+mm+"/"+yyyy;
                dob = dob.replace("th", "");
                dob = dob.replace("rd", "");
                dob = dob.replace("nd", "");
                break;
            }
        }
        return dob;
    }
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");

//    public List<AmlExtractionResponse> read_OFACSanctionsOnRussiaIndividuals2(String path, String harvestingLink){
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();

        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        JavascriptExecutor js = (JavascriptExecutor) driver;

        try {
            driver.get("https://home.treasury.gov/news/press-releases/jy0608");
            Thread.sleep(1000);

            try { // try1  Individuals
                String imp_dates = driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[1]/time")).getText().trim();
//                System.out.println(imp_dates);
                for (int i = 36; i <= 42; i++) {

                    for (int j=1;j<=2;j++) {
                        String name = "";
                        String summary = "";

                        try {
                            name = driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + i + "]/strong["+j+"]")).getText().trim();
                            if (!name.trim().isEmpty()) {
                                summary += driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + i + "]")).getText().trim() +
                                        ". " + driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + (i + 1) + "]")).getText().trim() +
                                        " " + driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + (i + 2) + "]")).getText().trim();
                            }
                        } catch (Exception e) {
                        }
                        name = name.replace(",","").trim();
                        if (!name.trim().isEmpty()) {
//                            AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();
                            if (!name.trim().isEmpty())
//                                amlExtractionResponse.setFullName(name.trim());
                                System.out.println(name);

                            if (!imp_dates.trim().isEmpty())
//                                amlExtractionResponse.setLastUpdatedAt(dOBTransformer(imp_dates.trim()));
                                System.out.println(imp_dates);

                            if (!summary.trim().isEmpty())
//                                amlExtractionResponse.setSummary(summary.trim());
                                System.out.println(summary);
                            System.out.println("-----------");

//                            amlExtractionResponse.setEntityType("Individual");
//                            amlExtractionResponse.setCategory("SANCTION");
//                            amlExtractionResponse.setRiskLevel("International");

//                            amlExtractionResponses.add(amlExtractionResponse);

                        }
                    }
                }
            }catch (Exception e){
                e.printStackTrace();
            } // try1 ends



            try { // try2  Individual
                String imp_dates =  driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[1]/time")).getText().trim();
                for (int i= 47; i<=49; i++){
                    for (int j=1;j<=2;j++) {
                        String name = "";
                        String summary = "";

                        try {
                            summary += driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + i + "]")).getText().trim();
                        } catch (Exception e) {
                        }

                        try {
                            name = driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[" + i + "]/strong["+j+"]")).getText().trim();
                        } catch (Exception e) {
                        }

                        try {
                            if (summary.contains("Andrey Sergeyevich Puchkov (Puchkov) and Yuriy Alekseyevich Soloviev (Soloviev)"))
                                summary += " " + driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[50]")).getText().trim();

                            if (summary.contains("Galina Olegovna Ulyutina"))
                                summary += " " + driver.findElement(By.xpath("//*[@id=\"block-hamilton-content\"]/article/div/div[2]/p[52]")).getText().trim();
                        }catch (Exception e){}

                        name = name.replace(",","").trim();
                        if (!name.trim().isEmpty()) {
//                            AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();
                            if (!name.trim().isEmpty())
//                                amlExtractionResponse.setFullName(name.trim());
                                System.out.println(name);

                            if (!imp_dates.trim().isEmpty())
//                                amlExtractionResponse.setLastUpdatedAt(dOBTransformer(imp_dates.trim()));
                                System.out.println(imp_dates);

                            if (!summary.trim().isEmpty())
//                                amlExtractionResponse.setSummary(summary.trim());
                                System.out.println(summary);
                            System.out.println("-----------");

//                            amlExtractionResponse.setEntityType("Individual");
//                            amlExtractionResponse.setCategory("SANCTION");
//                            amlExtractionResponse.setRiskLevel("International");

//                            amlExtractionResponses.add(amlExtractionResponse);

                        }
                    }
                }
            }catch (Exception e){}



        }catch (Exception e){}
        finally {
            driver.quit();
        }

//        return amlExtractionResponses;
    }
}