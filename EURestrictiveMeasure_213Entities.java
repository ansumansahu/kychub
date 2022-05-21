//package com.kychub.aml.v1.manualdatasources.headless;
//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class EURestrictiveMeasure_213Entities {

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
//    public List<AmlExtractionResponse> read_restrictive(String path, String harvestingLink) {
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        try {
            driver.get("https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02014D0145-20211213");
            Thread.sleep(4000);

            try {

                List<WebElement> table = driver.findElements(By.cssSelector("#docHtml > div:nth-child(74) > table > tbody > tr"));
                for (int i = 2; i <=table.size() ; i++) {

                    String name = "";
                    String aka = "";
                    String Identifyinginformation = "";
                    String StatementofReasons = "";
                    String Dateoflisting = "";
                    String Address = "";
                    String Telephone = "";
                    String Website = "";
                    String Email = "";
                    String extra = "";
                    String add ="";
//                    AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();

                    try {
                        Identifyinginformation = driver.findElement(By.cssSelector("#docHtml > div:nth-child(74) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(3)")).getText();
                    } catch (Exception e) {}

                    try {
                        name = driver.findElement(By.cssSelector("#docHtml > div:nth-child(74) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(2)")).getText();
                    } catch (Exception e) {}

                    try {
                        Dateoflisting = driver.findElement(By.cssSelector("#docHtml > div:nth-child(74) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(5)")).getText();
                    } catch (Exception e) {}

                    try {
                        StatementofReasons= driver.findElement(By.cssSelector("#docHtml > div:nth-child(74) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(4)")).getText();
                    } catch (Exception e) {}


                    try {
                        if(name.contains("(")){
                            aka=name.substring(name.indexOf("(")+1);
                            name=name.replace(aka,"");
                            name=name.replace(")","");
                            name=name.replace("(","");
                            aka=aka.replace(")","");
                            aka=aka.replace("(","");
                            aka=aka.replace("'","");
                            aka=aka.replace("formerly known as","");

                        }
                    }catch (Exception e){}

                    try {
                        String []split=Identifyinginformation.split("\n");

                        for (String z:split) {

                            if(z.contains("Address")){
                                z=z.replace("Address:","");
                                Address=z;
                                Address=Address.replaceAll("[^a-zA-Z0-9\\s]", "");
                            }else if(z.contains("Telephone")||z.contains("+")){
                                z=z.replace("Telephone",    "");
                                z=z.replace(":","");
                                Telephone=Telephone+z+", ";
                            }else if(z.contains("Website")||z.contains("http")||z.contains("www")){
                                z=z.replace("Website:","");
                                Website=Website+z+", ";
                            }else if(z.contains("Email")||z.contains("@")){
                                z=z.replace("Email:","");
                                z=z.replace("email","");
                                z=z.replace("or","");
                                Email=z;
                            }else {
                                extra=extra+z+", ";
                            }
                        }

                    }catch (Exception e){}

                    Dateoflisting=Dateoflisting.replace(".","/");

                    StatementofReasons=StatementofReasons.replace("\n"," ");
                    name=name.replace("'","");
                    name=name.replace("'","");
                    name=name.replaceAll("[^a-zA-Z0-9\\s]", "");
                    name=camelCasing(name);
                    name=name.replace("Socalled","");
                    name=name.replace("So Called","");
                    name=name.replace("‘","");
                    name=name.replace("’","");
                    aka=aka.replace("\n"," ");
                    aka=aka.replace("aka","");
                    aka=aka.replace("  ", "");
                    aka=aka.replaceAll("[^a-zA-Z0-9\\s]", "");
                    extra=extra.replace("Official information:,","");
                    extra=extra.replace(" Phone number:,","");
                    extra=extra.replace("Media resources:,","");
                    extra=extra.replace("Social media:,","");
                    extra=extra.replace("Social media and other information:,","");
                    extra=extra.replaceAll("[^a-zA-Z0-9\\s]", "");
                    StatementofReasons=StatementofReasons.replaceAll("[^a-zA-Z0-9\\s]", "");
                    extra=extra.replace("  ", "");


                    if (!name.trim().isEmpty()) {
//                        amlExtractionResponse.setFullName(name.trim());
                        System.out.println("fullName: "+name.trim());
                    }else{continue;}

                    if (!aka.trim().isEmpty()) {
//                        amlExtractionResponse.setAlias(aka.trim());
                        System.out.println("alias: "+aka.trim());
                    }
                    if (!StatementofReasons.trim().isEmpty()) {
                        add="Statement of Reasons: "+StatementofReasons.trim();
//                        amlExtractionResponse.setCause(StatementofReasons);
                        System.out.println("cause: "+StatementofReasons);
                    }
                    if (!Dateoflisting.trim().isEmpty()) {
//                        amlExtractionResponse.setListedOn(Dateoflisting.trim());
                        System.out.println("listedOn: "+Dateoflisting);
                    }
                    if (!Address.trim().isEmpty()) {
//                        amlExtractionResponse.setAddressLine1(Address.trim());
                        System.out.println("Address: "+Address.trim());
                    }
                    if (!Telephone.trim().isEmpty()) {
//                        amlExtractionResponse.setTelephoneNos(Telephone.trim());
                        System.out.println("telephoneNos: "+Telephone.trim());
                    }
                    if (!Website.trim().isEmpty()) {
//                        amlExtractionResponse.setWebsite(Website.trim());
                        System.out.println("Website: "+Website.trim());
                    }
                    if (!Email.trim().isEmpty()) {
//                        amlExtractionResponse.setEmails(Email.trim());
                        System.out.println("Emails: "+Email.trim());
                    }
                    if (!extra.trim().isEmpty()) {
//                        amlExtractionResponse.setAdditionalInfo(". Extra Identifying Information: "+extra.trim());
                        System.out.println("additionalInfo: "+extra);
                    }
                    String summary=name+" was found in the list of List of Persons under EU restrictive measures. Reasons: "+add;
//                    amlExtractionResponse.setSummary(summary);
                    System.out.println("summary: "+summary);

//                    amlExtractionResponses.add(amlExtractionResponse);

                }

            } catch (Exception e) {
            }

        } catch (Exception e) {
        } finally {
            driver.quit();
        }
//        return amlExtractionResponses;
    }
}