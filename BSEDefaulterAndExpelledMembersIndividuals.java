//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.List;

public class BSEDefaulterAndExpelledMembersIndividuals {
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");

//    public List<AmlExtractionResponse> read_BSEDefaulterAndExpelledMembersOrganisations(String path, String harvestingLink) {
//        List<AmlExtractionResponse> aml_extracts = new ArrayList<>();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--lang=en");
        options.addArguments("--headless");
        ChromeDriver driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        try {
            driver.get("https://www.bseindia.com/static/members/List_defaulters_Expelled_members.aspx/");

            String clg_no = "";
            String name = "";
            String date = "";
            String remarks = "";
            String exchange_notice = "";
            String public_notice = "";
            String additional_info = "";

            List<WebElement> entities = driver.findElements(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr/td[2]"));
//            System.out.println(entities.size());

            for (int i = 2; i <= entities.size(); i++) {
//                AmlExtractionResponse aml_extract = new AmlExtractionResponse();
                additional_info = "";
                String summary = "";
                try {
                    name = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[2]")).getText();
                    if (name.contains("Expelled") || name.contains("Defaulter") || (!name.contains("Ltd") && !name.contains("LTD") && !name.contains("Market") && !name.contains("Limited") && !name.contains("Securities")))
                        continue;
                    if (name.contains("Wealth Mantra Limited")) {
                        clg_no = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[1]")).getText();
                        date = "Defaulter Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[3]")).getText() + "; Expelled Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[23]/td[1]")).getText();
                        remarks = "Defaulter & Expelled";
                        exchange_notice = "Defaulter Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[5]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[5]/a[1]")).getAttribute("href") + "); Expelled Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[23]/td[3]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[23]/td[3]/a[1]")).getAttribute("href") + ")";
                        public_notice = "Defaulter Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[6]/a[1]")).getAttribute("href") + "); Expelled Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[22]/td[6]/a[1]")).getAttribute("href") + ")";

//                        aml_extract.setEntityType("Organisation");
//                        aml_extract.setRiskLevel("International");
//                        aml_extract.setCategory("Sanction");
//                        aml_extract.setNationality("Indian");
                        summary = name + " falls under the list of 'List of Members who have Declared Defaulter/Expelled since 1992' produced by BSE India. Clg. No.: " + clg_no;
//                        aml_extract.setFullName(name);
                        System.out.println(name);
//                        aml_extract.setImportantDates(date);
                        System.out.println(date);
                        summary = summary + ". Remarks: " + remarks;

                        if (!exchange_notice.isEmpty())
                            additional_info = additional_info + ". " + exchange_notice;
                        if (!public_notice.isEmpty())
                            additional_info = additional_info + ". " + public_notice;
//                        aml_extract.setSummary(summary);
                        System.out.println(summary);
                        if (!additional_info.isEmpty() && additional_info.charAt(0) == '.')
                            additional_info = additional_info.substring(1).trim();
//                        aml_extract.setAdditionalInfo(additional_info);
                        System.out.println(additional_info);
//                        aml_extract.setCountry("India");
                        System.out.println("-----------");

//                        aml_extracts.add(aml_extract);
                        continue;
                    }

                    if (name.contains("CPR Capital Services Limited")) {
                        clg_no = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[24]/td[1]")).getText();
                        date = "Defaulter Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[24]/td[3]")).getText() + "; Expelled Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[25]/td[1]")).getText();
                        remarks = "Defaulter & Expelled";
                        exchange_notice = "Defaulter Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[24]/td[5]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[24]/td[5]/a[1]")).getAttribute("href") + "); Expelled Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[25]/td[3]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[25]/td[3]/a[1]")).getAttribute("href") + ")";
                        public_notice = "Defaulter Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[24]/td[6]/a[1]")).getAttribute("href") + "); Expelled Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[25]/td[4]/a[1]")).getAttribute("href") + ")";

//                        aml_extract.setEntityType("Organisation");
//                        aml_extract.setRiskLevel("International");
//                        aml_extract.setCategory("Sanction");
//                        aml_extract.setNationality("Indian");
                        summary = name + " falls under the list of 'List of Members who have Declared Defaulter/Expelled since 1992' produced by BSE India. Clg. No.: " + clg_no;
//                        aml_extract.setFullName(name);
                        System.out.println(name);
//                        aml_extract.setImportantDates(date);
                        System.out.println(date);
                        summary = summary + ". Remarks: " + remarks;

                        if (!exchange_notice.isEmpty())
                            additional_info = additional_info + ". " + exchange_notice;
                        if (!public_notice.isEmpty())
                            additional_info = additional_info + ". " + public_notice;
//                        aml_extract.setSummary(summary);
                        System.out.println(summary);
                        if (!additional_info.isEmpty() && additional_info.charAt(0) == '.')
                            additional_info = additional_info.substring(1).trim();
//                        aml_extract.setAdditionalInfo(additional_info);
                        System.out.println(additional_info);
                        System.out.println("---------------");
//                        aml_extract.setCountry("India");

//                        aml_extracts.add(aml_extract);
                        continue;
                    }

                    if (name.contains("Kassa Finvest Pvt. Ltd")) {
                        clg_no = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[34]/td[1]")).getText();
                        date = "Defaulter Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[35]/td[1]")).getText() + "; Expelled Date: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[34]/td[3]")).getText();
                        remarks = "Defaulter & Expelled";
                        exchange_notice = "Defaulter Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[35]/td[3]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[35]/td[3]/a[1]")).getAttribute("href") + "); Expelled Exchange Notice: " + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[34]/td[5]/a[1]")).getText() + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[34]/td[5]/a[1]")).getAttribute("href") + ")";
                        public_notice = "Defaulter Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[35]/td[4]/a[1]")).getAttribute("href") + "); Expelled Public Notice: " + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[34]/td[6]/a[1]")).getAttribute("href") + ")";

//                        aml_extract.setEntityType("Organisation");
//                        aml_extract.setRiskLevel("International");
//                        aml_extract.setCategory("Sanction");
//                        aml_extract.setNationality("Indian");
                        summary = name + " falls under the list of 'List of Members who have Declared Defaulter/Expelled since 1992' produced by BSE India. Clg. No.: " + clg_no;
//                        aml_extract.setFullName(name);
                        System.out.println(name);
//                        aml_extract.setImportantDates(date);
                        summary = summary + ". Remarks: " + remarks;

                        if (!exchange_notice.isEmpty())
                            additional_info = additional_info + ". " + exchange_notice;
                        if (!public_notice.isEmpty())
                            additional_info = additional_info + ". " + public_notice;
//                        aml_extract.setSummary(summary);
                        if (!additional_info.isEmpty() && additional_info.charAt(0) == '.')
                            additional_info = additional_info.substring(1).trim();
//                        aml_extract.setAdditionalInfo(additional_info);
//                        aml_extract.setCountry("India");

//                        aml_extracts.add(aml_extract);
                        continue;
                    }

                }
                catch (Exception e) {
                    continue;
                }
                try {
                    clg_no = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[1]")).getText();
                }
                catch (Exception e) {
                    clg_no = "";
                }
                try {
                    date = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[3]")).getText();
                }
                catch (Exception e) {
                    date = "";
                }
                try {
                    remarks = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[4]")).getText();
                }
                catch (Exception e) {
                    remarks = "";
                }
                try {
                    exchange_notice = driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[5]/a[1]")).getText();
                    exchange_notice = exchange_notice + " (" + driver.findElement(By.xpath("/html[1]/body[1]/form[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[" + i + "]/td[5]/a[1]")).getAttribute("href") + ")";
                }
                catch (Exception e) {
                    exchange_notice = "";
                }
                try {
                    public_notice = " (" + driver.findElement(By.xpath("//*[@id=\"divmain\"]/div[3]/div/div/div/table/tbody/tr/td/table/tbody/tr[" + i + "]/td[6]/a")).getAttribute("href") + ")";
                }
                catch (Exception e) {
                    public_notice = "";
                }


//                aml_extract.setEntityType("Organisation");
//                aml_extract.setRiskLevel("International");
//                aml_extract.setCategory("Sanction");
//                aml_extract.setNationality("Indian");
                summary = name + " falls under the list of 'List of Members who have Declared Defaulter/Expelled since 1992' produced by BSE India. Clg. No.: " + clg_no;
//                aml_extract.setFullName(name);
                System.out.println(name);
//                aml_extract.setImportantDates("Date on which Declared Defaulter/Expelled: " + date);
                System.out.println(date);
                summary = summary + ". Remarks: " + remarks;

                if (!exchange_notice.isEmpty())
                    additional_info = additional_info + ". Exchange Notice: " + exchange_notice;
                if (!public_notice.isEmpty())
                    additional_info = additional_info + ". Public Notice: " + public_notice;
//                aml_extract.setSummary(summary);
                System.out.println(summary);
                if (!additional_info.isEmpty() && additional_info.charAt(0) == '.')
                    additional_info = additional_info.substring(1).trim();
//                aml_extract.setAdditionalInfo(additional_info);
                System.out.println(additional_info);
                System.out.println("===============");
//                aml_extract.setCountry("India");


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