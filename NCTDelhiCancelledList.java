//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.List;

public class NCTDelhiCancelledList {
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

//    public List<AmlExtractionResponse> read_NCTDelhiCancelledList(String path, String harvestingLink) {
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();

        ChromeOptions options = new ChromeOptions();
        options.addArguments("--lang=en");
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        try {
            driver.get("https://autho.dvat.gov.in/frmcancelleddealers.aspx");
            Thread.sleep(4000);

            List<WebElement> table = driver.findElements(By.xpath("/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr"));

            for (int i = 2; i <= table.size(); i++) {
                String zone = "";
                try {
                    zone = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr[" + i + "]/td[1]")).getText();
                    zone = zone.replace("Zone-", "");
                } catch (Exception e) {
                }

                List<WebElement> innertable = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr[" + i + "]/td[2]")).findElements(By.cssSelector("td a"));
                System.out.println(innertable.size());

                String link = "";

                for (WebElement z : innertable) {
                    link = link + " " + z.getAttribute("href") + "\n ";
                }

                String[] split = link.split("\n");
                for (String z : split) {
                    if (z == null) continue;
                    if (z.trim().isEmpty()) continue;

                    driver.get(z);
                    Thread.sleep(1000);

                    String ward = "";

                    try {
                        ward = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr[2]/td")).getText();
                        ward = ward.replace("Ward No.", "");
                        System.out.println("Ward: "+ward);
                    } catch (Exception e) {
                    }

                    if(ward.contains("Special")){
                        ward=ward+" Zone)";
                    }


                    List<WebElement> main = driver.findElements(By.xpath("/html/body/form/div[3]/table/tbody/tr"));
                    System.out.println(main.size());
                    for (int j = 4; j <= main.size(); j++) {
                        System.out.println(j);

                        String TIN = "";
                        String DealerName = "";
                        String DealerAddress = "";
                        String DateofCancellation = "";
                        String summary = "";

                        try {
                            TIN = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr[" + j + "]/td[2]")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            DealerName = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr[" + j + "]/td[3]")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            DealerAddress = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr[" + j + "]/td[4]")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            DateofCancellation = driver.findElement(By.xpath("/html/body/form/div[3]/table/tbody/tr[" + j + "]/td[5]")).getText();
                        } catch (Exception e) {
                        }

                        DealerAddress=DealerAddress.replace(",,",",");
                        DealerAddress = camelCasing(DealerAddress);
                        DealerName = camelCasing(DealerName);
                        summary=DealerName+" is in the List of Cancelled Dealers by Department of Trade & Taxes, Government of N.C.T. of Delhi (India).";

                        String additional_info = "";
                        if (!TIN.trim().isEmpty()) {
                            additional_info += "TIN: "+(TIN.trim());//additional
                        }
                        if (!ward.trim().isEmpty()) {
                            additional_info += "; Ward: "+(ward.trim());//additional
                        }
                        if (!zone.trim().isEmpty()) {
                            additional_info+= "; Zone: "+(zone.trim());//additional
                        }
                        if (additional_info.trim().startsWith("; "))
                            additional_info = additional_info.trim().substring(1).trim();


                        DealerAddress = DealerAddress.replace(",,", ",").trim();
                        if (DealerAddress.trim().endsWith(","))
                            DealerAddress = DealerAddress.trim().substring(0, DealerAddress.length()-1).trim();



                        if (!DealerName.trim().isEmpty()) {
//                            AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();

//                            amlExtractionResponse.setFullName(DealerName.trim());
                            System.out.println("FullName: "+DealerName);

                            if (!summary.trim().isEmpty()) {
//                                amlExtractionResponse.setSummary(summary.trim());
                                System.out.println("summary: "+summary);
                            }
                            if (!additional_info.trim().isEmpty()) {
//                                amlExtractionResponse.setAdditionalInfo(additional_info.trim());
                                System.out.println("additional_info: "+additional_info);
                            }
                            if (!DealerAddress.trim().isEmpty()) {
//                                amlExtractionResponse.setAddressLine1(DealerAddress.trim());
                                System.out.println("DealerAddress: "+DealerAddress);
                            }
                            if (!DateofCancellation.trim().isEmpty()) {
//                                amlExtractionResponse.setImportantDates("Date of Cancellation: "+DateofCancellation.trim());//important dates
                                System.out.println("DateofCancellation: "+DateofCancellation);
                            }
//                            amlExtractionResponse.setCountry("India");
                            System.out.println("------------------------");

//                            amlExtractionResponses.add(amlExtractionResponse);
                        }

                    }

                    driver.navigate().back();

                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            driver.quit();
        }

//        return amlExtractionResponses;
    }
}