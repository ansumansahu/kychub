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

public class EURestrictiveMeasure_337Entities{

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
            driver.get("https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022D0337");
            Thread.sleep(4000);

            try {

                List<WebElement> table = driver.findElements(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr"));

                for (int i = 2; i <=table.size() ; i++) {

                    String name = "";
                    String russian_name = "";
                    String Identifyinginformation = "";
                    String StatementofReasons = "";
                    String Dateoflisting = "";
                    String Address = "";
                    String Telephone = "";
                    String Website = "";
                    String Email = "";
//                    AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();
                    String summary ="";
                    String add="";


                    try {
                        Identifyinginformation = driver.findElement(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr:nth-of-type("+i+") td:nth-of-type(3)")).getText();
                    } catch (Exception e) {}

                    try {
                        name = driver.findElement(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr:nth-of-type("+i+") td:nth-of-type(2)")).getText();
                    } catch (Exception e) {}

                    try {
                        Dateoflisting = driver.findElement(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr:nth-of-type("+i+") td:nth-of-type(5)")).getText();
                    } catch (Exception e) {}

                    try {
                        StatementofReasons= driver.findElement(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr:nth-of-type("+i+") td:nth-of-type(4)")).getText();
                    } catch (Exception e) {}

                    try {
                        String temp=driver.findElement(By.cssSelector("table:nth-of-type(2) table.oj-table tbody tr:nth-of-type("+(i+1)+") td:nth-of-type(2)")).getText();
                        if(temp.trim().isEmpty()) {
                            StatementofReasons=StatementofReasons + driver.findElement(By.cssSelector("table:nth-of-type(1) table.oj-table tbody tr:nth-of-type("+(i+1)+") td:nth-of-type(4)")).getText();
                            i++;
                        }

                    }catch (Exception e){}

                    try {
                        if(name.contains("(")){
                            russian_name=name.substring(name.indexOf("(")+1);
                            name=name.replace(russian_name,"");
                            name=name.replace(")","");
                            name=name.replace("(","");
                        }
                    }catch (Exception e){}

                    try {
                        String []split=Identifyinginformation.split("\n");

                        for (String z:split) {

                            if(z.contains("Address")){
                                z=z.replace("Address:","");
                                Address=z;
                            }else if(z.contains("Telephone")){
                                z=z.replace("Telephone","");
                                z=z.replace(":","");
                                Telephone=z;
                            }else if(z.contains("Website")){
                                z=z.replace("Website:","");
                                Website=z;
                            }else if(z.contains("Email")){
                                z=z.replace("Email:","");
                                Email=z;
                            }else {
                                Telephone=Telephone+z+", ";
                            }
                        }

                    }catch (Exception e){}

                    Dateoflisting=Dateoflisting.replace(".","/");
                    StatementofReasons=StatementofReasons.replaceAll("[^a-zA-Z0-9\\s]", "");
                    StatementofReasons=StatementofReasons.replace("\n"," ");
                    name=camelCasing(name);

                    if (!name.trim().isEmpty()) {
//                        amlExtractionResponse.setFullName(name.trim());
                        System.out.println(name);
                    }
                    if (!StatementofReasons.trim().isEmpty()) {
                        add="Statement of Reasons: "+StatementofReasons.trim();
//                        amlExtractionResponse.setCause(StatementofReasons);
                        System.out.println(StatementofReasons);
                    }
                    if (!Dateoflisting.trim().isEmpty()) {
//                        amlExtractionResponse.setListedOn(Dateoflisting.trim());
                        System.out.println(Dateoflisting);
                    }
                    if (!Address.trim().isEmpty()) {
//                        amlExtractionResponse.setAddressLine1(Address.trim());
                        System.out.println(Address);
                    }
                    if (!Telephone.trim().isEmpty()) {
//                        amlExtractionResponse.setTelephoneNos(Telephone.trim());
                        System.out.println(Telephone);
                    }
                    if (!Website.trim().isEmpty()) {
//                        amlExtractionResponse.setWebsite(Website.trim());
                        System.out.println(Website);
                    }
                    if (!Email.trim().isEmpty()) {
//                        amlExtractionResponse.setEmails(Email.trim());
                        System.out.println(Email);
                    }


                    summary=name+" was found in the list of List of Persons under EU restrictive measures.";
//                    amlExtractionResponse.setSummary(summary);
                    System.out.println(summary);
//                    amlExtractionResponse.setAdditionalInfo(add);
                    System.out.println(add);

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