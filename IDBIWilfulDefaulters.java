//package com.kychub.aml.v1.manualdatasources.headless;

//import com.kychub.aml.v1.model.AmlExtractionResponse;
import org.apache.poi.ss.usermodel.DataFormatter;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;

public class IDBIWilfulDefaulters {
    public static void main(String[] args){
//    public List<AmlExtractionResponse> read_IDBIWilfulDefaulters(String path, String harvestingLink){
//        List<AmlExtractionResponse> amlExtractionResponses = new ArrayList<>();
        File src = new File("C:\\Users\\Ansh\\Downloads\\WillfulDefaulters-as-on-March082019.xlsx");

        try{
//            System.out.println(src.isFile());
            DataFormatter dataFormatter = new DataFormatter();

            FileInputStream fis = new FileInputStream(src);
            XSSFWorkbook wb = new XSSFWorkbook(fis);

            XSSFSheet sheet = wb.getSheetAt(0);
            int lastRowNum = sheet.getLastRowNum();
//            System.out.println(lastRowNum);
//            System.out.println(sheet.getRow(4).getLastCellNum());
            for (int i=5; i<=lastRowNum; i++){

//                AmlExtractionResponse amlExtractionResponse = new AmlExtractionResponse();

                String SCTG = dataFormatter.formatCellValue(sheet.getRow(i).getCell(0, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String BKNM = dataFormatter.formatCellValue(sheet.getRow(i).getCell(1, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String BKBR = dataFormatter.formatCellValue(sheet.getRow(i).getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String STATE = dataFormatter.formatCellValue(sheet.getRow(i).getCell(3, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String srNo = dataFormatter.formatCellValue(sheet.getRow(i).getCell(4, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String PARTY = dataFormatter.formatCellValue(sheet.getRow(i).getCell(5, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String REGADDR = dataFormatter.formatCellValue(sheet.getRow(i).getCell(6, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String OSAMT = dataFormatter.formatCellValue(sheet.getRow(i).getCell(7, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String SUIT = dataFormatter.formatCellValue(sheet.getRow(i).getCell(8, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String OTHER_BK = dataFormatter.formatCellValue(sheet.getRow(i).getCell(9, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR1 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(10, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR1 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(11, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR2 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(12, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR2 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(13, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR3 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(14, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR3 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(15, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR4 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(16, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR4 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(17, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR5 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(18, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR5 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(19, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR6 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(20, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR6 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(21, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR7 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(22, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR7 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(23, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR8 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(24, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR8 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(25, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR9 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(26, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR9 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(27, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR10 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(28, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR10 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(29, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR11 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(30, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR11 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(31, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR12 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(32, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR12 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(33, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR13 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(34, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR13 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(35, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR14 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(36, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR14 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(37, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR15 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(38, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR15 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(39, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR16 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(40, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR16 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(41, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR17 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(42, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR17 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(43, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR18 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(44, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR18 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(45, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIR19 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(46, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();
                String DIN_DIR19 = dataFormatter.formatCellValue(sheet.getRow(i).getCell(47, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK)).trim();



                if (SCTG.trim().isEmpty())
                    break;

                if (!BKNM.isEmpty() && !BKNM.equals("--") && !BKNM.equals("NA") && !BKNM.equals("-")){

                }
                else
                    BKNM = "";

                if (!BKBR.isEmpty() && !BKBR.equals("--") && !BKBR.equals("NA") && !BKBR.equals("-"))
                    BKBR = BKBR.replace("\n", " ");
                else
                    BKBR = "";

                if (!STATE.isEmpty() && !STATE.equals("--") && !STATE.equals("NA") && !STATE.equals("-"))
                    STATE=STATE.replace("\n", " ");
                else
                    STATE = "";

                if (!srNo.isEmpty() && !srNo.equals("--") && !srNo.equals("NA") && !srNo.equals("-"))
                    srNo = srNo.replace("\n", " ");
                else
                    srNo = "";

                if (!PARTY.isEmpty() && !PARTY.equals("--") && !PARTY.equals("NA") && !PARTY.equals("-"))
                    PARTY = PARTY.replace("\n", " ");
                else
                    PARTY = "";

                if (!REGADDR.isEmpty() && !REGADDR.equals("--") && !REGADDR.equals("NA") && !REGADDR.equals("-"))
                    REGADDR = REGADDR.replace("\n", " ");
                else
                    REGADDR = "";

                if (!OSAMT.isEmpty() && !OSAMT.equals("--") && !OSAMT.equals("NA") && !OSAMT.equals("-"))
                    OSAMT = OSAMT.replace("\n", " ");
                else
                    OSAMT = "";

                if (!SUIT.isEmpty() && !SUIT.equals("--") && !SUIT.equals("NA") && !SUIT.equals("-"))
                    SUIT = SUIT.replace("\n", " ");
                else
                    SUIT = "";

                if (!OTHER_BK.isEmpty() && !OTHER_BK.equals("--") && !OTHER_BK.equals("NA") && !OTHER_BK.equals("-") && !OTHER_BK.equals("No") && !OTHER_BK.equals("None")){
                    OTHER_BK = (OTHER_BK.replaceAll("\n", ", ").replaceAll("\\s{2,}", " "));
                    OTHER_BK = "("+OTHER_BK+")";
                }
                else
                    OTHER_BK = "";

                if (!DIR1.isEmpty() && !DIR1.equals("--") && !DIR1.equals("NA") && !DIR1.equals("-"))
                    DIR1 = DIR1.replace("\n", " ");
                else
                    DIR1 = "";

                if (!DIN_DIR1.isEmpty() && !DIN_DIR1.equals("--") && !DIN_DIR1.equals("NA") && !DIN_DIR1.equals("-"))
                    DIN_DIR1 = DIN_DIR1.replace("\n", " ").replaceAll("'", "");
                else
                    DIN_DIR1 = "";

                if (!DIR2.isEmpty() && !DIR2.equals("--") && !DIR2.equals("NA") && !DIR2.equals("-"))
                    DIR2 = DIR2.replace("\n", " ");
                else
                    DIR2 = "";

                if (!DIN_DIR2.isEmpty() && !DIN_DIR2.equals("--") && !DIN_DIR2.equals("NA") && !DIN_DIR2.equals("-"))
                    DIN_DIR2 = DIN_DIR2.replaceAll("'", "");
                else
                    DIN_DIR2 = "";

                if (!DIR3.isEmpty() && !DIR3.equals("--") && !DIR3.equals("NA") && !DIR3.equals("-"))
                    DIR3 = DIR3.replace("\n", " ");
                else
                    DIR3 = "";

                if (!DIN_DIR3.isEmpty() && !DIN_DIR3.equals("--") && !DIN_DIR3.equals("NA") && !DIN_DIR3.equals("-"))
                    DIN_DIR3 = DIN_DIR3.replaceAll("'", "");
                else
                    DIN_DIR3 = "";

                if (!DIR4.isEmpty() && !DIR4.equals("--") && !DIR4.equals("NA") && !DIR4.equals("-"))
                    DIR4 = DIR4.replace("\n", " ");
                else
                    DIR4 = "";

                if (!DIN_DIR4.isEmpty() && !DIN_DIR4.equals("--") && !DIN_DIR4.equals("NA") && !DIN_DIR4.equals("-"))
                    DIN_DIR4 = DIN_DIR4.replaceAll("'", "");
                else
                    DIN_DIR4 = "";

                if (!DIR5.isEmpty() && !DIR5.equals("--") && !DIR5.equals("NA") && !DIR5.equals("-"))
                    DIR5 = DIR5.replace("\n", " ");
                else
                    DIR5 = "";

                if (!DIN_DIR5.isEmpty() && !DIN_DIR5.equals("--") && !DIN_DIR5.equals("NA") && !DIN_DIR5.equals("-"))
                    DIN_DIR5 = DIN_DIR5.replace("\n", " ");
                else
                    DIN_DIR5 = "";

                if (!DIR6.isEmpty() && !DIR6.equals("--") && !DIR6.equals("NA") && !DIR6.equals("-"))
                    DIR6 = DIR6.replace("\n", " ");
                else
                    DIR6 = "";

                if (!DIN_DIR6.isEmpty() && !DIN_DIR6.equals("--") && !DIN_DIR6.equals("NA") && !DIN_DIR6.equals("-"))
                    DIN_DIR6 = DIN_DIR6.replace("\n", " ");
                else
                    DIN_DIR6 = "";

                if (!DIR7.isEmpty() && !DIR7.equals("--") && !DIR7.equals("NA") && !DIR7.equals("-"))
                    DIR7 = DIR7.replace("\n", " ");
                else
                    DIR7 = "";

                if (!DIN_DIR7.isEmpty() && !DIN_DIR7.equals("--") && !DIN_DIR7.equals("NA") && !DIN_DIR7.equals("-"))
                    DIN_DIR7 = DIN_DIR7.replace("\n", " ");
                else
                    DIN_DIR7 = "";

                if (!DIR8.isEmpty() && !DIR8.equals("--") && !DIR8.equals("NA") && !DIR8.equals("-"))
                    DIR8 = DIR8.replace("\n", " ");
                else
                    DIR8 = "";

                if (!DIN_DIR8.isEmpty() && !DIN_DIR8.equals("--") && !DIN_DIR8.equals("NA") && !DIN_DIR8.equals("-"))
                    DIN_DIR8 = DIN_DIR8.replace("\n", " ");
                else
                    DIN_DIR8 = "";

                if (!DIR9.isEmpty() && !DIR9.equals("--") && !DIR9.equals("NA") && !DIR9.equals("-"))
                    DIR9 = DIR9.replace("\n", " ");
                else
                    DIR9 = "";

                if (!DIN_DIR9.isEmpty() && !DIN_DIR9.equals("--") && !DIN_DIR9.equals("NA") && !DIN_DIR9.equals("-"))
                    DIN_DIR9 = DIN_DIR9.replace("\n", " ");
                else
                    DIN_DIR9 = "";

                if (!DIR10.isEmpty() && !DIR10.equals("--") && !DIR10.equals("NA") && !DIR10.equals("-"))
                    DIR10 = DIR10.replace("\n", " ");
                else
                    DIR10 = "";

                if (!DIN_DIR10.isEmpty() && !DIN_DIR10.equals("--") && !DIN_DIR10.equals("NA") && !DIN_DIR10.equals("-"))
                    DIN_DIR10 = DIN_DIR10.replace("\n", " ");
                else
                    DIN_DIR10 = "";

                if (!DIR11.isEmpty() && !DIR11.equals("--") && !DIR11.equals("NA") && !DIR11.equals("-"))
                    DIR11 = DIR11.replace("\n", " ");
                else
                    DIR11 = "";

                if (!DIN_DIR11.trim().isEmpty() && !DIN_DIR11.trim().equals("--") && !DIN_DIR11.equals("NA") && !DIN_DIR11.equals("-"))
                    DIN_DIR11 = DIN_DIR11.replace("\n", " ");
                else
                    DIN_DIR11 = "";

                if (!DIR12.isEmpty() && !DIR12.equals("--") && !DIR12.equals("NA") && !DIR12.equals("-"))
                    DIR12 = DIR12.replace("\n", " ");
                else
                    DIR12 = "";

                if (!DIN_DIR12.isEmpty() && !DIN_DIR12.equals("--") && !DIN_DIR12.equals("NA") && !DIN_DIR12.equals("-"))
                    DIN_DIR12 = DIN_DIR12.replace("\n", " ");
                else
                    DIN_DIR12 = "";

                if (!DIR13.isEmpty() && !DIR13.equals("--") && !DIR13.equals("NA") && !DIR13.equals("-"))
                    DIR13 = DIR13.replace("\n", " ");
                else
                    DIR13 = "";

                if (!DIN_DIR13.isEmpty() && !DIN_DIR13.equals("--") && !DIN_DIR13.equals("NA") && !DIN_DIR13.equals("-"))
                    DIN_DIR13 = DIN_DIR13.replace("\n", " ");
                else
                    DIN_DIR13 = "";

                if (!DIR14.isEmpty() && !DIR14.equals("--") && !DIR14.equals("NA") && !DIR14.equals("-"))
                    DIR14 = DIR14.replace("\n", " ");
                else
                    DIR14 = "";

                if (!DIN_DIR14.isEmpty() && !DIN_DIR14.equals("--") && !DIN_DIR14.equals("NA") && !DIN_DIR14.equals("-"))
                    DIN_DIR14 = DIN_DIR14.replace("\n", " ");
                else
                    DIN_DIR14 = "";

                if (!DIR15.isEmpty() && !DIR15.equals("--") && !DIR15.equals("NA") && !DIR15.equals("-"))
                    DIR15 = DIR15.replace("\n", " ");
                else
                    DIR15 = "";

                if (!DIN_DIR15.isEmpty() && !DIN_DIR15.equals("--") && !DIN_DIR15.equals("NA") && !DIN_DIR15.equals("-"))
                    DIN_DIR15 = DIN_DIR15.replace("\n", " ");
                else
                    DIN_DIR15 = "";

                if (!DIR16.isEmpty() && !DIR16.equals("--") && !DIR16.equals("NA") && !DIR16.equals("-"))
                    DIR16 = DIR16.replace("\n", " ");
                else
                    DIR16 = "";

                if (!DIN_DIR16.isEmpty() && !DIN_DIR16.equals("--") && !DIN_DIR16.equals("NA") && !DIN_DIR16.equals("-"))
                    DIN_DIR16 = DIN_DIR16.replace("\n", " ");
                else
                    DIN_DIR16 = "";

                if (!DIR17.isEmpty() && !DIR17.equals("--") && !DIR17.equals("NA") && !DIR17.equals("-"))
                    DIR17 = DIR17.replace("\n", " ");
                else
                    DIR17 = "";

                if (!DIN_DIR17.isEmpty() && !DIN_DIR17.equals("--") && !DIN_DIR17.equals("NA") && !DIN_DIR17.equals("-"))
                    DIN_DIR17 = DIN_DIR17.replace("\n", " ");
                else
                    DIN_DIR17 = "";

                if (!DIR18.isEmpty() && !DIR18.equals("--") && !DIR18.equals("NA") && !DIR18.equals("-"))
                    DIR18 = DIR18.replace("\n", " ");
                else
                    DIR18 = "";

                if (!DIN_DIR18.isEmpty() && !DIN_DIR18.equals("--") && !DIN_DIR18.equals("NA") && !DIN_DIR18.equals("-"))
                    DIN_DIR18 = DIN_DIR18.replace("\n", " ");
                else
                    DIN_DIR18 = "";

                if (!DIR19.isEmpty() && !DIR19.equals("--") && !DIR19.equals("NA") && !DIR19.equals("-"))
                    DIR19 = DIR19.replace("\n", " ");
                else
                    DIR19 = "";

                if (!DIN_DIR19.isEmpty() && !DIN_DIR19.equals("--") && !DIN_DIR19.equals("NA") && !DIN_DIR19.equals("-"))
                    DIN_DIR19 = DIN_DIR19.replace("\n", " ");
                else
                    DIN_DIR19 = "";

                String additional_info ="Suit: "+SUIT;

                if (!OTHER_BK.isEmpty())
                    additional_info += ", Other Bank: "+OTHER_BK;

                if (!DIN_DIR1.trim().isEmpty())
                    additional_info +=", Director1 Id: "+DIN_DIR1.trim();
                if (!DIR1.trim().isEmpty())
                    additional_info +=", Director1: "+DIR1.trim();

                if (!DIN_DIR2.trim().isEmpty())
                    additional_info +=", Director2 Id: "+DIN_DIR2.trim();
                if (!DIR2.trim().isEmpty())
                    additional_info +=", Director2: "+DIR2.trim();

                if (!DIN_DIR3.trim().isEmpty())
                    additional_info +=", Director3 Id: "+DIN_DIR3.trim();
                if (!DIR3.trim().isEmpty())
                    additional_info +=", Director3: "+DIR3.trim();

                if (!DIN_DIR4.trim().isEmpty())
                    additional_info +=", Director4 Id: "+DIN_DIR4.trim();
                if (!DIR4.trim().isEmpty())
                    additional_info +=", Director4: "+DIR4.trim();

                if (!DIN_DIR5.trim().isEmpty())
                    additional_info +=", Director5 Id: "+DIN_DIR5.trim();
                if (!DIR5.trim().isEmpty())
                    additional_info +=", Director5: "+DIR5.trim();

                if (!DIN_DIR6.trim().isEmpty())
                    additional_info +=", Director6 Id: "+DIN_DIR6.trim();
                if (!DIR6.trim().isEmpty())
                    additional_info +=", Director6: "+DIR6.trim();

                if (!DIN_DIR7.trim().isEmpty())
                    additional_info +=", Director7 Id: "+DIN_DIR7.trim();
                if (!DIR7.trim().isEmpty())
                    additional_info +=", Director7: "+DIR7.trim();

                if (!DIN_DIR8.trim().isEmpty())
                    additional_info +=", Director8 Id: "+DIN_DIR8.trim();
                if (!DIR8.trim().isEmpty())
                    additional_info +=", Director8: "+DIR8.trim();

                if (!DIN_DIR9.trim().isEmpty())
                    additional_info +=", Director9 Id: "+DIN_DIR9.trim();
                if (!DIR9.trim().isEmpty())
                    additional_info +=", Director9: "+DIR9.trim();

                if (!DIN_DIR10.trim().isEmpty())
                    additional_info +=", Director10 Id: "+DIN_DIR10.trim();
                if (!DIR10.trim().isEmpty())
                    additional_info +=", Director10: "+DIR10.trim();

                if (!DIN_DIR11.trim().isEmpty())
                    additional_info +=", Director11 Id: "+DIN_DIR11.trim();
                if (!DIR11.trim().isEmpty())
                    additional_info +=", Director11: "+DIR11.trim();

                if (!DIN_DIR12.trim().isEmpty())
                    additional_info +=", Director12 Id: "+DIN_DIR12.trim();
                if (!DIR12.trim().isEmpty())
                    additional_info +=", Director12: "+DIR12.trim();

                if (!DIN_DIR13.trim().isEmpty())
                    additional_info +=", Director13 Id: "+DIN_DIR13.trim();
                if (!DIR13.trim().isEmpty())
                    additional_info +=", Director13: "+DIR13.trim();

                if (!DIN_DIR14.trim().isEmpty())
                    additional_info +=", Director14 Id: "+DIN_DIR14.trim();
                if (!DIR14.trim().isEmpty())
                    additional_info +=", Director14: "+DIR14.trim();

                if (!DIN_DIR15.trim().isEmpty())
                    additional_info +=", Director15 Id: "+DIN_DIR15.trim();
                if (!DIR15.trim().isEmpty())
                    additional_info +=", Director15: "+DIR15.trim();

                if (!DIN_DIR16.trim().isEmpty())
                    additional_info +=", Director16 Id: "+DIN_DIR16.trim();
                if (!DIR16.trim().isEmpty())
                    additional_info +=", Director16: "+DIR16.trim();

                if (!DIN_DIR17.trim().isEmpty())
                    additional_info +=", Director17 Id: "+DIN_DIR17.trim();
                if (!DIR17.trim().isEmpty())
                    additional_info +=", Director17: "+DIR17.trim();

                if (!DIN_DIR18.trim().isEmpty())
                    additional_info +=", Director18 Id: "+DIN_DIR18.trim();
                if (!DIR18.trim().isEmpty())
                    additional_info +=", Director18: "+DIR18.trim();

                if (!DIN_DIR19.trim().isEmpty())
                    additional_info +=", Director19 Id: "+DIN_DIR19.trim();
                if (!DIR19.trim().isEmpty())
                    additional_info +=", Director19: "+DIR19.trim();

                String summary = PARTY+" is a willfull defaulter in "+BKNM+" "+BKBR+" branch with outstanding amount = Rs. "+OSAMT;
//                amlExtractionResponse.setSummary(PARTY+" is a willfull defaulter in "+BKNM+" "+BKBR+" branch with outstanding amount = Rs. "+OSAMT);   //summary
//                amlExtractionResponse.setFullName(PARTY);
                System.out.println("name: "+PARTY);
//                amlExtractionResponse.setAddressLine1(REGADDR);
                System.out.println("address: "+REGADDR);
//                amlExtractionResponse.setState(STATE);
                System.out.println(STATE);
//                amlExtractionResponse.setEntityType("Organization");
//                amlExtractionResponse.setCategory("Sanction");
//                amlExtractionResponse.setNationality("Indian");
//                amlExtractionResponse.setCountry("India");
//                amlExtractionResponse.setRiskLevel("National");
//                amlExtractionResponse.setAdditionalInfo(additional_info);
                System.out.println(additional_info);
                System.out.println(summary);
                System.out.println("--------------------------");

//                amlExtractionResponses.add(amlExtractionResponse);

            }


        }
        catch (Exception e){
            e.printStackTrace();
        }


//        return amlExtractionResponses;
    }
}