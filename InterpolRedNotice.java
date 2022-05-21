//package com.kychub.aml.v1.manualdatasources.headless;
//
//import com.kychub.aml.v1.model.AmlExtractionResponse;
//import com.kychub.aml.v1.model.entity.Dob;
//import org.apache.commons.text.WordUtils;
import org.openqa.selenium.*;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class InterpolRedNotice {
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");
//    public List<AmlExtractionResponse> read_InterpolRedNotice(String path, String harvestingLink) {
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        WebDriverWait wait = new WebDriverWait(driver, 15);
        try {
            driver.get("https://www.interpol.int/How-we-work/Notices/View-Red-Notices");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            try {
                driver.findElement(By.xpath("//a[@id='privacy-cookie-banner__privacy-close']")).click();
            } catch (NoSuchElementException e) {
            }
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//select[@id='nationality']")));
            Select select = new Select(driver.findElement(By.xpath("//select[@id='nationality']")));
            List<WebElement> allOptions = select.getOptions();
            String xpath1 = "//button[@id='submit']";
            for (WebElement option : allOptions) {

                String counrtyValue = option.getAttribute("value");
//                if (counrtyValue.equalsIgnoreCase("IN")) {
                if (!counrtyValue.trim().isEmpty()) {
                    select.selectByValue(counrtyValue);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    driver.findElement(By.xpath(xpath1)).click();
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    boolean isVisibleNext = true;
                    while (isVisibleNext) {
                        List<WebElement> listOfMembers = new ArrayList<>();
                        listOfMembers = driver.findElements(By.xpath("//*[@id='noticesResultsItemList']/div/div/div/div[2]/div[1]/a"));
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
//                        System.out.println(listOfMembers.size());
                        for (int i = 1; i <= listOfMembers.size(); i++) {
//                            AmlExtractionResponse aer = new AmlExtractionResponse();
                            try {
                                Thread.sleep(2000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                            String link = "";
                            try {
                                link = driver.findElement(By.xpath("//*[@id='noticesResultsItemList']/div[" + i + "]/div/div/div[2]/div[1]/a")).getAttribute("href");
                            } catch (NoSuchElementException e) {
//
                            }
//                            String detailsUrl = wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//*[@id='noticesResultsItemList']/div[" + i + "]/div/div/div[2]/div[1]/a"))).getAttribute("data-singleurl");
                            ((JavascriptExecutor) driver).executeScript("window.open();");
                            Set<String> tabs = driver.getWindowHandles();
                            driver.switchTo().window(tabs.toArray()[1].toString());
                            try {
                                Thread.sleep(1000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }

                            boolean isURLWorking;
                            if (!link.isEmpty()) {
                                try {
//                                    System.out.println("--------------");
                                    driver.get(link);
                                    wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//h1[@class='bannerWantedSingle__title']")));
                                    String nametest = driver.findElement(By.xpath("//h1[@class='bannerWantedSingle__title']")).getText();
                                    isURLWorking = true;
                                } catch (Exception e) {

                                    driver.quit();
                                    driver.switchTo().window(tabs.toArray()[0].toString());
                                    isURLWorking = false;
                                }
                                if (isURLWorking) {
                                    try {
                                        wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//body/div[@class='content']/div[@id='singlePanel']/div[@class='container']/div[@class='wantedsingle__wrappercolumns']/div[@class='wantedsingle__colleft js-gallery']/div[@class='redNoticeLargePhoto redNoticeLargePhoto--red']/div[@class='redNoticeLargePhoto__wrapperImg']/img[1]")));
                                        String imgURL = driver.findElement(By.xpath("//body/div[@class='content']/div[@id='singlePanel']/div[@class='container']/div[@class='wantedsingle__wrappercolumns']/div[@class='wantedsingle__colleft js-gallery']/div[@class='redNoticeLargePhoto redNoticeLargePhoto--red']/div[@class='redNoticeLargePhoto__wrapperImg']/img[1]")).getAttribute("src");
//                                        aer.setImage(imgURL);
                                    } catch (TimeoutException e) {
//
                                    }
                                    String nameAsPage = driver.findElement(By.xpath("//h1[@class='bannerWantedSingle__title']")).getText();
                                    String[] nameOfPerson = nameAsPage.split(",");
                                    String name = "";
                                    if (nameOfPerson.length > 1) {
                                        name = nameOfPerson[nameOfPerson.length - 1] + " " + nameOfPerson[0];
                                    } else {
                                        name = nameOfPerson[0];
                                    }
//                                    aer.setFullName(WordUtils.capitalizeFully(name.replace("'", "").toLowerCase().trim()));
                                    System.out.println("Fullname: " + name);
//                                    aer.setRawNameFromSource(WordUtils.capitalizeFully(nameAsPage.replace("'", "").toLowerCase().trim()));
                                    String wantedBy = "";
                                    try {
                                        wantedBy = driver.findElement(By.xpath("//p[@class='bannerWantedSingle__wantedBy']")).getText().replace("\n", " ").trim();

                                    } catch (NoSuchElementException e) {
                                    }
                                    List<WebElement> identityInfoTable = driver.findElements(By.xpath("//div[@class='wantedsingle__infosWrapper']//table//tr"));
                                    for (int j = 1; j <= identityInfoTable.size(); j++) {
                                        String key = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper']//table//tr[" + j + "]//td[1]")).getText();
                                        String value = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper']//table//tr[" + j + "]//td[2]/strong")).getText();

                                        if (!value.isEmpty()) {
                                            if (key.equalsIgnoreCase("Family name")) {
//                                                aer.setLastName(WordUtils.capitalizeFully(value.replace("'", "").toLowerCase().trim()));
                                                System.out.println("Lastname: " + value);
                                            } else if (key.equalsIgnoreCase("Forename")) {
//                                                aer.setFirstName(WordUtils.capitalizeFully(value.replace("'", "").toLowerCase().trim()));
                                                System.out.println("Firstname: " + value);
                                            } else if (key.equalsIgnoreCase("Name in original script")) {
                                                // aer.setOriginal(value);
                                            } else if (key.equalsIgnoreCase("Gender")) {
//                                                aer.setGender(value);
                                                System.out.println("gender: " + value);
                                            } else if (key.equalsIgnoreCase("Date of birth")) {
                                                System.out.println("dob: " + value);
//                                                List<Dob> dobList = new ArrayList<>();
//                                                Dob dob = new Dob();
//                                                SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
//                                                try {
//                                                    dob.setDob(dateFormat.parse(value));
//                                                    dob.setQuality("EXACT");
//                                                    dobList.add(dob);
//                                                    aer.setListOfDob(dobList);
//                                                } catch (ParseException e) {
//                                                    String birthYear = value.replaceAll("//", "").trim();
//                                                    dob.setDobYear(Integer.valueOf(birthYear));
//                                                    dob.setQuality("ONLY YEAR");
//                                                    dobList.add(dob);
//                                                    aer.setListOfDob(dobList);
//                                                }
                                            } else if (key.equalsIgnoreCase("Place of birth")) {
//                                                aer.setPlaceOfBirthCountry(WordUtils.capitalizeFully(value.toLowerCase().trim()));
                                                System.out.println("pob_country: " + value);
                                            } else if (key.equalsIgnoreCase("Nationality")) {
//                                                String[] nationalityArray = value.split(", ");
//                                                if (nationalityArray.length >= 2) {
//                                                    aer.setNationality(WordUtils.capitalizeFully(nationalityArray[0].toLowerCase().trim()));
//                                                } else {
//                                                    aer.setNationality(WordUtils.capitalizeFully(nationalityArray[0].toLowerCase().trim()));
//                                                }
                                                System.out.println("nation: " + value);
                                            } else if (key.equalsIgnoreCase("Distinguishing marks and characteristics")) {
//                                                aer.setDistinguishMarks(value);
                                                System.out.println("marks: " + value);
                                            }
//                                            String strName = "";
//                                            if (aer.getFirstName() != null) {
//                                                strName = aer.getFirstName();
//                                            }
//                                            if(aer.getLastName() != null) {
//                                                strName += " " + aer.getLastName();
//                                            }
                                            // aer.setFullName(strName.trim());
                                            // System.out.println(aer.getFullName());

                                        }
                                    }
                                    List<WebElement> pysicalInfoTable = driver.findElements(By.xpath("//div[@class='wantedsingle__infosWrapper physicalDescriptionContent']//tr"));
                                    for (int n = 1; n <= pysicalInfoTable.size(); n++) {
                                        String key2 = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper physicalDescriptionContent']//tr[" + n + "]//td[1]")).getText();

                                        String value2 = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper physicalDescriptionContent']//tr[" + n + "]//td[2]/strong")).getText();

                                        if (!value2.isEmpty()) {
                                            if (key2.equalsIgnoreCase("Height")) {
//                                                aer.setHeight(value2);
                                                System.out.println("height: " + value2);
                                            } else if (key2.equalsIgnoreCase("Weight")) {
//                                                aer.setWeight(value2);
                                                System.out.println("weight: " + value2);
                                            } else if (key2.equalsIgnoreCase("Colour of hair")) {
//                                                aer.setHair(value2);
                                                System.out.println("hair: " + value2);
                                            } else if (key2.equalsIgnoreCase("Colour of eyes")) {
//                                                aer.setEyes(value2);
                                                System.out.println("eyes: " + value2);
                                            }
                                        }
                                    }
                                    List<WebElement> detailsInfoTable = driver.findElements(By.xpath("//div[@class='wantedsingle__infosWrapper detailsContent']//tr"));
                                    for (int m = 1; m <= detailsInfoTable.size(); m++) {
                                        String key3 = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper detailsContent']//tr[" + m + "]//td[1]")).getText();
                                        String value3 = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper detailsContent']//tr[" + m + "]//td[2]/strong")).getText();

                                        if (!value3.isEmpty()) {
                                            if (key3.equalsIgnoreCase("Language(s) spoken")) {
//                                                aer.setLanguagesKnown(value3);
                                                System.out.println("LanguagesKnown: " + value3);
                                            }
//
                                        }
                                    }
                                    try {
                                        String associates = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper associatesContent']/div")).getText();
                                        if (!associates.isEmpty()) {
                                            // logger.info(associates);
                                        }
                                    } catch (NoSuchElementException e) {
                                    }

                                    try {
                                        String charges = driver.findElement(By.xpath("//div[@class='wantedsingle__infosWrapper warrantContent']")).getText();
//                                        aer.setCharges(charges);
                                        System.out.println("charges: " + charges);
                                    } catch (NoSuchElementException e) {
                                    }
//                                    aer.setSummary("Interpole Red Notice: " + wantedBy);
//                                    aer.setEntityType("Individual");
//                                    amlExtractionResponses.add(aer);
//                                    System.out.println(amlExtractionResponses.size());
                                    driver.close();
                                    driver.switchTo().window(tabs.toArray()[0].toString());
                                }
                            }
                        }
//                        else{
//                                driver.quit();
//                            driver.switchTo().window(tabs.toArray()[1].toString());
//                            }
//                        }
                        try {
                            driver.findElement(By.xpath("//a[@class='nextIndex right-arrow']")).click();
                            isVisibleNext = true;
                            Thread.sleep(3000);
                        } catch (Exception ec) {
                            try {
                                driver.findElement(By.xpath("//li[@class='nextElement hidden']"));
                                isVisibleNext = false;
                            } catch (Exception e) {
                                isVisibleNext = false;
                            }

                        }

                    }

                }//li[@class='nextElement hidden']
                // }
            }
        }
        catch ( Exception e){
            e.printStackTrace();
        }
        finally {
            driver.quit();
        }
//        return amlExtractionResponses;
    }
}