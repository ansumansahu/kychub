//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
public class FBIMostWanted {
//    public List<AmlExtractionResponse> read_FBIMostWanted(String path, String harvestingLink) {
//        List<AmlExtractionResponse> aml_extracts = new ArrayList<>();
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");
        ChromeOptions options = new ChromeOptions();
        ChromeDriver driver = new ChromeDriver(options);
        options.addArguments("--headless");
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);

        try {
            driver.get("https://www.fbi.gov/wanted");

            List<WebElement> outer = driver.findElements(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/a[1]/div[1]/img[1]"));

            for (int i = 1; i <= (outer.size() - 1); i++) {
                driver.findElement(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[" + i + "]/a[1]/div[1]/img[1]")).click();

                try {
                    Thread.sleep(500);
                }
                catch (Exception e) {

                }

                List<WebElement> inner = null;
                if (i <= 2)
                    inner = driver.findElements(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/ul[1]/li/a[1]/div[1]/img[1]"));

                else
                    inner = driver.findElements(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/ul[1]/li/a[1]/div[1]/img[1]"));

                for (int j = 1; j <= inner.size(); j++) {
//                    AmlExtractionResponse aml_extract = new AmlExtractionResponse();
                    if (i <= 2)
                        try {
                            driver.findElement(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[" + j + "]/a[1]/div[1]/img[1]")).click();
                        }
                        catch(Exception e){
                            continue;
                        }
                    else
                        try {
                            driver.findElement(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[" + j + "]/a[1]/div[1]/img[1]")).click();
                        }
                        catch (Exception e){
                            continue;
                        }

                    try {
                        Thread.sleep(600);
                    }
                    catch (Exception e) {

                    }

                    try {
                        driver.findElement(By.xpath("/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/a[1]")).click();
                    }
                    catch (Exception e) {

                    }

                    try {
                        Thread.sleep(500);
                    }
                    catch (Exception e) {

                    }

                    //Extraction
                    String additional_info = "";
                    String summary = "";

                    try {
                        String image = driver.findElement(By.xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/section[1]/article[1]/section[2]/div[1]/div[1]/div[2]/div[1]/img[1]")).getAttribute("src");
//                        aml_extract.setImage(image);
                        System.out.println("image: "+image);
                    }
                    catch (Exception e) {
                    }
                    try {
                        String full_name = driver.findElement(By.className("documentFirstHeading")).getText();
//                        aml_extract.setFullName(full_name);
                        System.out.println("full_name: "+full_name);
                    }
                    catch (Exception e) {
                        continue;
                    }
                    try {
                        summary = driver.findElement(By.className("summary")).getText();
                        if (driver.getCurrentUrl().contains("/kidnap/"))
                            summary = "Kidnapped/Missing: " + summary;
                    }
                    catch (Exception e) {
                    }
                    try {
                        String wanted_for = driver.findElement(By.className("wanted-person-caution")).getText().split("\n")[1];
                        summary = summary + ". " + "Wanted for: " + wanted_for;
                    }
                    catch (Exception e) {
                    }
                    try {
                        String alias = driver.findElement(By.className("wanted-person-aliases")).getText().split("\n")[1];
//                        aml_extract.setAlias(alias);
                        System.out.println("alias: "+alias);
                    }
                    catch (Exception e) {
                    }
                    try {
                        String alias_DOB = "";
                        String POB_city = "";
                        String hair = "";
                        String eyes = "";
                        String height = "";
                        String weight = "";
                        String complexion = "";
                        String gender = "";
                        String race = "";
                        String designation = "";
                        String buildCharacteristic = "";
                        String nationality = "";
                        String marks = "";
                        String ncic = "";
                        String languages = "";
                        List<WebElement> description = driver.findElements(By.tagName("tr"));
                        for (WebElement attribute : description) {
                            if (attribute.getText().startsWith("Date")) {
                                alias_DOB = attribute.getText();
                                alias_DOB = alias_DOB.substring(alias_DOB.indexOf("Used") + 5);
//                                aml_extract.setAliasDOb(alias_DOB);
                                additional_info = additional_info + "Date(s) of Birth Used: " + alias_DOB + "; ";
                                continue;
                            }
                            if (attribute.getText().startsWith("Place")) {
                                POB_city = attribute.getText();
                                POB_city = POB_city.substring(POB_city.indexOf("Birth") + 6);
//                                aml_extract.setPlaceOfBirthCity(POB_city);
                                System.out.println("POB_city: "+POB_city);
                                continue;
                            }
                            if (attribute.getText().startsWith("Hair")) {
                                hair = attribute.getText();
                                hair = hair.substring(5);
//                            aml_extract.setHair(hair);
                                System.out.println("hair: "+hair);
                                continue;
                            }
                            if (attribute.getText().startsWith("Eyes")) {
                                eyes = attribute.getText();
                                eyes = eyes.substring(5);
//                            aml_extract.setEyes(eyes);
                                System.out.println("eyes: "+eyes);
                                continue;
                            }
                            if (attribute.getText().startsWith("Height")) {
                                height = attribute.getText();
                                height = height.substring(7);
                                String temp_height = "";
                                for (int k = 0; k < height.length(); k++) {
                                    char ch = height.charAt(k);
                                    if (ch == '\'') {
                                        temp_height = temp_height + "feet" + " ";
                                    }
                                    else if (ch == '\"') {
                                        temp_height = temp_height + "inches" + " ";
                                    }
                                    else if (Character.isDigit(ch)) {
                                        temp_height = temp_height + ch + " ";
                                    }
                                    else {
                                        temp_height = temp_height + ch;
                                    }
                                }
                                height = temp_height.trim();
//                            aml_extract.setHeight(height);
                                System.out.println("height: "+height);
                                continue;
                            }
                            if (attribute.getText().startsWith("Weight")) {
                                weight = attribute.getText();
                                weight = weight.substring(7);
//                            aml_extract.setWeight(weight);
                                System.out.println("weight: "+weight);
                                continue;
                            }
                            if (attribute.getText().startsWith("Build")) {
                                buildCharacteristic = attribute.getText();
                                buildCharacteristic = buildCharacteristic.substring(6);
//                                aml_extract.setBuildCharacteristic(buildCharacteristic);
                                System.out.println("buildCharacteristic: "+buildCharacteristic);
                                continue;
                            }
                            if (attribute.getText().startsWith("Complex")) {
                                complexion = attribute.getText();
                                complexion = complexion.substring(11);
//                                aml_extract.setWeight(complexion);
                                System.out.println("complexion: "+complexion);
                                continue;
                            }
                            if (attribute.getText().startsWith("Sex")) {
                                gender = attribute.getText();
                                gender = gender.substring(4);
//                                aml_extract.setGender(gender);
                                System.out.println("gender: "+gender);
                                continue;
                            }
                            if (attribute.getText().startsWith("Race")) {
                                race = attribute.getText();
                                race = race.substring(5);
//                            aml_extract.setRace(race);
                                System.out.println("race: "+race);
                                continue;
                            }
                            if (attribute.getText().startsWith("Occu")) {
                                designation = attribute.getText();
                                designation = designation.substring(11);
//                                aml_extract.setDesignation(designation);
                                System.out.println("designation: "+designation);
                                continue;
                            }
                            if (attribute.getText().startsWith("Nation")) {
                                nationality = attribute.getText();
                                nationality = nationality.substring(12);
//                                aml_extract.setNationality(nationality);
                                System.out.println("nationality: "+nationality);
                                continue;
                            }
                            if (attribute.getText().startsWith("Scars")) {
                                marks = attribute.getText();
                                marks = marks.substring(marks.indexOf("Marks") + 6);
//                            aml_extract.setDistinguishMarks(marks);
                                System.out.println("marks: "+marks);
                                additional_info = additional_info + "Scars and Marks: " + marks + "; ";
                                continue;
                            }
                            if (attribute.getText().startsWith("NCIC")) {
                                ncic = attribute.getText();
                                ncic = ncic.substring(5);
                                additional_info = additional_info + "National Crime Information Center(NCIC): " + ncic + "; ";
                                continue;
                            }
                            if (attribute.getText().startsWith("Languages")) {
                                languages = attribute.getText();
                                languages = languages.substring(10);
//                                aml_extract.setLanguagesKnown(languages);
                                System.out.println("languages: "+languages);
                                continue;
                            }
                            if (attribute.getText().startsWith("Citizenship")) {
                                nationality = attribute.getText();
                                nationality = nationality.substring(12);
//                                aml_extract.setNationality(nationality);
                                System.out.println("nationality: "+nationality);
                                continue;
                            }

                        }
                    }
                    catch (Exception e) {
                    }

                    try {
                        String reward = driver.findElement(By.className("wanted-person-reward")).getText().split("\n")[1];
//                        aml_extract.setReward(reward);
                        System.out.println("reward: "+reward);
                    }
                    catch (Exception e) {
                    }
                    try {
                        String remarks = driver.findElement(By.className("wanted-person-remarks")).getText().split("\n")[1];
//                        aml_extract.setRemarks(remarks);
                        System.out.println("remarks: "+remarks);
                    }
                    catch (Exception e) {
                    }
                    try {
                        String details = driver.findElement(By.className("wanted-person-details")).getText();
                        details = details.substring(details.indexOf("\n") + 1);
                        summary = summary + ". " + details;
                    }
                    catch (Exception e) {
                    }

//                    aml_extract.setEntityType("Individual");
//                    aml_extract.setCountry("United States of America");
//                    if (!driver.getCurrentUrl().contains("/kidnap/")) {
//                        aml_extract.setCategory("Crime");
//                        aml_extract.setRiskLevel("International");
//                    }
//                    aml_extract.setSummary(summary);
                    System.out.println("Summary: "+summary);
                    if (!additional_info.isEmpty())
                        additional_info = additional_info.substring(0, additional_info.length() - 2);
//                    aml_extract.setAdditionalInfo(additional_info);
                    System.out.println("AdditionalInfo: "+additional_info);



//                    aml_extracts.add(aml_extract);

                    driver.navigate().back();

                    try {
                        Thread.sleep(200);
                    }
                    catch (Exception e) {

                    }
                    try {
                        driver.findElement(By.xpath("/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/a[1]")).click();
                    }
                    catch (Exception e) {

                    }

                }
                driver.navigate().back();
                try {
                    Thread.sleep(200);
                }
                catch (Exception e) {

                }
                try {
                    driver.findElement(By.xpath("/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/a[1]")).click();
                }
                catch (Exception e) {

                }
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