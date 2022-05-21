import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;

public class OFSIConsolidatedListRussia {
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
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        try {
            driver.get("https://sanctionssearch.ofsi.hmtreasury.gov.uk/");
            Thread.sleep(4000);
            try {
                WebElement search=driver.findElement(By.cssSelector("input.form-control.ng-untouched.ng-pristine.ng-valid"));
                search.sendKeys("ukraine");
                Thread.sleep(2000);
                driver.findElement(By.id("btnSearch")).click();
                Thread.sleep(10000);

            }catch (Exception e){}

            while(true) {

                try {

                    List<WebElement> table = driver.findElements(By.cssSelector("tbody tr"));

                    for (WebElement z : table) {

                        String groupid = "";
                        String name = "";
                        String regime = "";
                        String status = "";
                        String type = "";
                        String Nationality = "";
                        String Address = "";
                        String PostZipCode = "";
                        String Country = "";
                        String DOB = "";
                        String TownofBirth = "";
                        String CountryofBirth = "";
                        String Position = "";
                        String PassportDetails = "";
                        String NationalIdentificationNumber = "";
                        String DateListed = "";
                        String GroupLastUpdated = "";
                        String OtherInformation = "";
                        String add = "";

                        try {
                            groupid = z.findElement(By.cssSelector("td:nth-of-type(1)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            name = z.findElement(By.cssSelector("td:nth-of-type(2)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            regime = z.findElement(By.cssSelector("td:nth-of-type(3)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            status = z.findElement(By.cssSelector("td:nth-of-type(4)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            type = z.findElement(By.cssSelector("td:nth-of-type(5)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            Nationality = z.findElement(By.cssSelector("td:nth-of-type(6)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            Address = z.findElement(By.cssSelector("td:nth-of-type(7)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            PostZipCode = z.findElement(By.cssSelector("td:nth-of-type(8)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            Country = z.findElement(By.cssSelector("td:nth-of-type(9)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            DOB = z.findElement(By.cssSelector("td:nth-of-type(10)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            TownofBirth = z.findElement(By.cssSelector("td:nth-of-type(11)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            CountryofBirth = z.findElement(By.cssSelector("td:nth-of-type(12)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            Position = z.findElement(By.cssSelector("td:nth-of-type(13)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            PassportDetails = z.findElement(By.cssSelector("td:nth-of-type(14)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            NationalIdentificationNumber = z.findElement(By.cssSelector("td:nth-of-type(15)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            DateListed = z.findElement(By.cssSelector("td:nth-of-type(16)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            GroupLastUpdated = z.findElement(By.cssSelector("td:nth-of-type(17)")).getText();
                        } catch (Exception e) {
                        }

                        try {
                            OtherInformation = z.findElement(By.cssSelector("td:nth-of-type(18)")).getText();
                        } catch (Exception e) {
                        }


                        if (!groupid.trim().isEmpty()) {
                            add=add+"Group ID: "+groupid.trim()+". ";
                        }
                        if (!name.trim().isEmpty()) {
//                            amlExtractionResponse.setFullName(name.trim());
                            System.out.println("name: "+name);
                        }
                        if (!regime.trim().isEmpty()) {
                            add=add+"Regime: "+regime.trim()+". ";

                        }
                        if (!status.trim().isEmpty()) {
//                            amlExtractionResponse.setStatus(status);
                            System.out.println("status: "+status);
                        }
//                        if (!type.trim().isEmpty()) {
//                            amlExtractionResponse.setEntityType(type.trim());
//                        }
                        if (!Nationality.trim().isEmpty()) {
//                            amlExtractionResponse.setNationality(Nationality.trim());
                            System.out.println("Nationality: "+Nationality);
                        }
                        if (!Address.trim().isEmpty()) {
//                            amlExtractionResponse.setAddressLine1(Address.trim());
                            System.out.println("Address: "+Address);
                        }
                        if (!PostZipCode.trim().isEmpty()) {
//                            amlExtractionResponse.setPostalCode(PostZipCode.trim());
                            System.out.println("PostZipCode: "+PostZipCode);
                        }
                        if (!Country.trim().isEmpty()) {
//                            amlExtractionResponse.setCountry(Country.trim());
                            System.out.println("Country: "+Country);
                        }
                        if (!DOB.trim().isEmpty()) {
//                            amlExtractionResponse.setDob(DOB.trim());
                            System.out.println("DOB: "+DOB);
                        }
                        if (!TownofBirth.trim().isEmpty()) {
//                            amlExtractionResponse.setPlaceOfBirthCity(TownofBirth.trim());
                            System.out.println("TownofBirth: "+TownofBirth);
                        }
                        if (!CountryofBirth.trim().isEmpty()) {
//                            amlExtractionResponse.setPlaceOfBirthCountry(CountryofBirth.trim());
                            System.out.println("CountryofBirth: "+CountryofBirth);
                        }
                        if (!Position.trim().isEmpty()) {
//                            amlExtractionResponse.setDesignation(Position.trim());
                            System.out.println("Position: "+Position);
                        }
                        if (!PassportDetails.trim().isEmpty()) {
                            add=add+"Passport Details: "+PassportDetails.trim()+". ";
                        }
                        if (!NationalIdentificationNumber.trim().isEmpty()) {
                            add=add+"National Identification Number: "+NationalIdentificationNumber.trim()+". ";
                        }
                        if (!DateListed.trim().isEmpty()) {
//                            amlExtractionResponse.setListedOn(DateListed.trim());
                            System.out.println("DateListed: "+DateListed);
                        }
                        if (!GroupLastUpdated.trim().isEmpty()) {
//                            amlExtractionResponse.setLastUpdatedAt(GroupLastUpdated.trim());
                            System.out.println("GroupLastUpdated: "+GroupLastUpdated);
                        }
                        if (!OtherInformation.trim().isEmpty()) {
                            add = add+OtherInformation;
                        }
//                        String summary = amlExtractionResponse.getFullName()+" has been sanctioned by Office of Financil Sanctions Implmentation HM Treasury";
//                        amlExtractionResponse.setAdditionalInfo(add);
                        System.out.println("AdditionalInfo: "+add);
//                        amlExtractionResponse.setSummary(summary);
//                        amlExtractionResponses.add(amlExtractionResponse);
//                        System.out.println(amlExtractionResponses.size());


                    }

                } catch (Exception e) {}

                try {

                    driver.findElement(By.cssSelector(".btn-group  button#Next")).click();

                    Thread.sleep(10000);

                }catch (Exception e){
                    break;
                }


            }


        } catch (Exception e) {
        } finally {
            driver.quit();
        }
    }
}