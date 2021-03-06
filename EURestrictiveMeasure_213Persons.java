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

public class EURestrictiveMeasure_213Persons {
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
                List<WebElement> table = driver.findElements(By.cssSelector("#docHtml > div:nth-child(69) > table > tbody > tr"));
                for (int i = 3; i <=table.size() ; i++) {

                    try {

                        String temp=driver.findElement(By.cssSelector("#docHtml > div:nth-child(69) > table > tbody > tr td:nth-child(2)")).getText();
                        if(temp==null) continue;

                    }catch (Exception e){
                        continue;
                    }

                    String name = "";
                    String extra_name = "";
                    String Identifyinginformation = "";
                    String Reasons = "";
                    String DOB = "";
                    String POB = "";
                    String Nationality = "";
                    String Gender = "";
                    String Function="";
                    String Associates="";
                    String summary="";
                    String Address="";
                    String TelephoneNos="";
                    String Passport="";
//                    AmlExtractionResponse amlExtractionResponse= new AmlExtractionResponse();


                    try {
                        Identifyinginformation = driver.findElement(By.cssSelector("#docHtml > div:nth-child(69) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(3)")).getText();
                    } catch (Exception e) {}

                    try {
                        name = driver.findElement(By.cssSelector("#docHtml > div:nth-child(69) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(2)")).getText();
                    } catch (Exception e) {}


                    try {
                        Reasons= driver.findElement(By.cssSelector("#docHtml > div:nth-child(69) > table > tbody > tr:nth-of-type("+i+") td:nth-of-type(4)")).getText();
                    } catch (Exception e) {}


                    try {
                        if(name.contains("(")){
                            extra_name=name.substring(name.indexOf("(")+1);
                            name=name.replace(extra_name,"");
                            name=name.replace(")","");
                            name=name.replace("(","");
                            extra_name=extra_name.replace(")","");

                        }
                    }catch (Exception e){}

                    try {
                        String []split=Identifyinginformation.split("\n");

                        for (String z:split) {

                            if(z.contains("DOB")){
                                z=z.replace("DOB:","");
                                DOB=z;
                            }else if(z.contains("POB")){
                                z=z.replace("POB","");
                                z=z.replace(":","");
                                POB=z;
                            }else if(z.contains("Function")){
                                z=z.replace("Function:","");
                                Function=z;
                            }else if(z.contains("Gender")){
                                z=z.replace("Gender:","");
                                Gender=z;
                            }else if(z.contains("Nationality")){
                                z=z.replace("Nationality:","");
                                Nationality=z;
                            }else if(z.contains("Associates")){
                                z=z.replace("Associates:","");
                                Associates=z;
                            }
                            else if(z.contains("Address")){
                                z=z.replace("Address:","");
                                Address=z;
                            }
                            else if(z.contains("Passport")){
                                z=z.split(":")[1];
                                Passport=z;
                            }
                            else if(z.contains("Tel.")){
                                z=z.replace("Tel.","");
                                TelephoneNos=z;
                            }
                        }

                    }catch (Exception e){}

                    DOB=DOB.replace(".","/");
                    extra_name=extra_name.replace("\n","");
                    extra_name=extra_name.replace("a.k.a","");
                    Reasons=Reasons.replaceAll("[^a-zA-Z0-9\\s]", "");


                    Reasons=Reasons.replace("\n"," ");
                    name=camelCasing(name);
                    summary=name+" was found in the list of List of entities under EU restrictive measures.";

                    if (!name.trim().isEmpty()) {
//                        amlExtractionResponse.setFullName(name.trim());
                        System.out.println("name: "+name);
                    }else{continue;}
//                    if (!extra_name.trim().isEmpty()) {
//                        amlExtractionResponse.setRawNameFromSource(extra_name.trim());
//                        System.out.println("extra_name: "+extra_name);
//                    }
                    if (!Reasons.trim().isEmpty()) {
//                        amlExtractionResponse.setCause(Reasons.trim());
                        System.out.println("Reasons: "+Reasons);
//                        amlExtractionResponse.setSummary(summary+" Reasons: "+Reasons.trim());
                    }
                    if (!DOB.trim().isEmpty()) {
//                        amlExtractionResponse.setDob(DOB.trim());
                        System.out.println("DOB: "+DOB);
                    }
                    if (!POB.trim().isEmpty()) {
//                        amlExtractionResponse.setPlaceOfBirthCity(POB);
                        System.out.println("POB: "+POB);
                    }
                    if (!Function.trim().isEmpty()) {
//                        amlExtractionResponse.setAdditionalInfo("Function: "+Function.trim()+".");
                        System.out.println("Function: "+Function);
                    }
                    if (!Gender.trim().isEmpty()) {
//                        amlExtractionResponse.setGender(Gender.trim());
                        System.out.println("Gender: "+Gender);
                    }
                    if (!Nationality.trim().isEmpty()) {
//                        amlExtractionResponse.setNationality(Nationality.trim());
                        System.out.println("Nationality: "+Nationality);
                    }
                    if (!Address.trim().isEmpty()) {
//                        amlExtractionResponse.setFullAddress(Address.trim());
                        System.out.println("Address: "+Address);
                    }
                    if (!TelephoneNos.trim().isEmpty()) {
//                        amlExtractionResponse.setTelephoneNos(TelephoneNos.trim());
                        System.out.println("TelephoneNos: "+TelephoneNos);
                    }
                    if (!Passport.trim().isEmpty()) {
//                        amlExtractionResponse.setAdditionalInfo(amlExtractionResponse.getAdditionalInfo()+". Passport: "+Passport.trim());
                        System.out.println("Passport: "+Passport);
                    }
                    if (!Associates.trim().isEmpty()) {
//                        amlExtractionResponse.setAdditionalInfo(amlExtractionResponse.getAdditionalInfo()+". Associates: "+Associates.trim());
                        System.out.println("Associates: "+Associates);
                    }
                    System.out.println("-------------------");

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