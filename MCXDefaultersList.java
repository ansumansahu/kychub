import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
public class MCXDefaultersList {
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe");
        ChromeOptions options = new ChromeOptions();
        ChromeDriver driver = new ChromeDriver(options);
//        options.addArguments("--headless");
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        try {
            Thread.sleep(2000);
            driver.get("https://www.mcxindia.com/Investor-Services/defaulters/defaulters-list");
            Thread.sleep(2000);
            List<WebElement> table = driver.findElements(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/div/div/a"));
            int i = 1;
            while(i <= table.size()) {
                try {
                    //WebElement el1 = driver.findElement(By.xpath("//*[@id=\"menu0.1body\"]/div[1]/a"));
                    Actions actions = new Actions(driver);
                    //actions.moveToElement(el);
//                    actions.moveToElement(el).click().perform();
//                    Thread.sleep(2000);
                    List<WebElement> list = driver.findElements(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr"));
                    System.out.println(list.size());
                    for (int j = 2; j <= list.size(); j++) {
                        String Defaulter_Name = "";
                        String Member_ID = "";
                        String Date_of_Declaration = "";
                        String Date_of_Publication = "";
                        String Data = "";
                        String Summary = "";
                        String Category = "Watchlist";
                        String Entity_Type = "Organization";
                        String Country = "India";
                        String Risk_level = "National";
                        String Additional = "";
                        String name = driver.findElement(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr[" + j + "]/td[1]")).getText();
                        Defaulter_Name = name;
                        String ID = driver.findElement(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr[" + j + "]/td[2]")).getText();
                        Member_ID = ID;
                        String declaration = driver.findElement(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr[" + j + "]/td[3]")).getText();
                        Date_of_Declaration = declaration;
                        String publication = driver.findElement(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr[" + j + "]/td[4]")).getText();
                        Date_of_Publication = publication;
                        String summary = Defaulter_Name + "'s name is in the list of Defaulter companies according to the MCX(Metal and Energy), a multi commodity exchange of India";
                        Summary = summary;
                        WebElement pdf = driver.findElement(By.xpath("/html/body/form/div[3]/div[3]/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr[" + j + "]/td[5]/a"));
                        String src = pdf.getAttribute("href");
                        Data = src;
                        if (Member_ID.isEmpty() == false) {
                            if (Additional.isEmpty() == false) {
                                Additional += "; Member ID: " + Member_ID;
                            } else
                                Additional += "Member ID: " + Member_ID;
                        }
                        if (Date_of_Declaration.isEmpty() == false) {
                            if (Additional.isEmpty() == false) {
                                Additional += "; Date of Declaration: " + Date_of_Declaration;
                            } else
                                Additional += "Date of Declaration: " + Date_of_Declaration;
                        }
                        if (Date_of_Publication.isEmpty() == false) {
                            if (Additional.isEmpty() == false) {
                                Additional += "; Date of Publication: " + Date_of_Publication;
                            } else
                                Additional += "Date of Publication: " + Date_of_Publication;
                        }
                        if (Data.isEmpty() == false) {
                            if (Additional.isEmpty() == false) {
                                Additional += "; Detailed PDF: " + Data;
                            } else
                                Additional += "Detailed PDF: " + Data;
                        }
                        if (Defaulter_Name.isEmpty() == false) {
                            System.out.println("name: "+Defaulter_Name);;
                            if (Additional.isEmpty() == false) {
                                System.out.println("additionalInfo: "+Additional);;
                            }
                            if (Defaulter_Name.isEmpty() == false) {
                                System.out.println("summary: "+summary);;
                            }
//                            if (Defaulter_Name.trim().isEmpty() == false) {
//                                response.setEntityType(Entity_Type);
//                            }
//                            if (Defaulter_Name.trim().isEmpty() == false) {
//                                response.setCountry(Country);
//                            }
//                            if (Defaulter_Name.trim().isEmpty() == false) {
//                                response.setCategory(Category);
//                            }
//                            if (Defaulter_Name.trim().isEmpty() == false) {
//                                response.setRiskLevel(Risk_level);
//                            }
                        }
                    }
                    i++;
//                    System.out.println(i);
                    driver.findElement(By.cssSelector("#cph_InnerContainerMiddleContent1_ctl00_ctl00_ctl00_pager_ctl00_ctl00_numeric > a:nth-child(" +i+ ")")).click();
                    Thread.sleep(10000);

                } catch (Exception e) {
                    break;
                }
            }
        } catch (Exception e) {
        } finally {
            driver.quit();
        }
    }
}