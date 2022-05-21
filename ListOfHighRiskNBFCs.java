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

public class ListOfHighRiskNBFCs {
    public static void main(String[] args){
//    public List<AmlExtractionResponse> read_ListOfDefaulters(String path, String harvestingLink) {
//        List<AmlExtractionResponse> aml_extracts = new ArrayList<>();
        File src = new File("C:\\Users\\Ansh\\Downloads\\List-of-High-Risk-NBFCs-as-on-31.01.2018.xlsx");

        try {
//            System.out.println(src.isFile());
            DataFormatter dataFormatter = new DataFormatter();

            FileInputStream fis = new FileInputStream(src);
            XSSFWorkbook wb = new XSSFWorkbook(fis);

            XSSFSheet sheet = wb.getSheetAt(0);
            int lastRowNum = sheet.getLastRowNum();
//            System.out.println(lastRowNum + "\n");
            for (int i = 3; i <= lastRowNum; i++) {

//               String sr_no = "";
                String name = "";

//               try {
//                   sr_no = dataFormatter.formatCellValue(sheet.getRow(i).getCell(0, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK));
//                   if (sr_no.isEmpty())
//                       continue;
//               }
//               catch (Exception e) {
//                   continue;
//               }

                try {
                    name = dataFormatter.formatCellValue(sheet.getRow(i).getCell(1, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK));
                    if (name.isEmpty())
                        continue;
                    name = name.replaceAll("\n", " ");
//                    name = fix(name);
                }
                catch (Exception e) {
                    continue;
                }


//                AmlExtractionResponse aml_extract = new AmlExtractionResponse();

//                aml_extract.setEntityType("Organisation");
//                aml_extract.setCategory("Watchlist");
//                aml_extract.setRiskLevel("International");
//                aml_extract.setNationality("Indian");
//                aml_extract.setFullName(name);
                System.out.println(name);
//                aml_extract.setSummary("Falls under the list of Non Banking Financial Companies categorized as 'High Risk Financial Institutions' (by FIU-IND) on account of non compliance with PMLA and PML Rules, i.e., non registration of Principal Officer (PO) as on 31.01.2018");
//                aml_extract.setCountry("India");

//                aml_extracts.add(aml_extract);

            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }

//        return aml_extracts;
    }
    private String fix(String name) {
        String new_name = "";
        name = name.replaceAll("  ", " ");
        name = name.replaceAll("\\.", ". ");
        name = name.replaceAll("  ", " ");
        name = name.trim();
        String[] arr = name.split(" ");
        for (String str : arr) {
            new_name = new_name + Character.toUpperCase(str.charAt(0)) + str.substring(1).toLowerCase() + " ";
        }
        return  new_name;
    }
}