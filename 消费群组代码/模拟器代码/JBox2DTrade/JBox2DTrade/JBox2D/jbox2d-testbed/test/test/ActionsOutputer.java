package test;

import java.util.ArrayList;
import java.util.List;
import java.io.*;

public class ActionsOutputer {
	public static String write_tarpath = "actionData/";
	public static String cust_tarpath = "custData/cust_people_action.csv"; 
		
	public static void writeCSV(List<Integer> actionList, int ctimes, int id) throws IOException {
		String tarFile = write_tarpath + ctimes + "_" + id + ".csv";
		File file = new File(tarFile);
		if(!file.exists()) file.createNewFile();
		BufferedWriter bw = new BufferedWriter(new FileWriter(tarFile));
		String s = "";
		for (Integer actionNum : actionList) {
			s += actionNum + ",";
		}
		s = s.substring(0, s.length()-1);
		//System.out.println(s);
		bw.write(s);
		bw.flush();
		bw.close();
	}
	
	public static void customize() throws IOException{
		List<Integer> custList = new ArrayList<Integer>();
		String read_tarFile = cust_tarpath;
		
		File file = new File(read_tarFile);	
		if(!file.exists()) file.createNewFile();
		
		BufferedReader br = new BufferedReader(new FileReader(read_tarFile));
		String tmp;
		while((tmp = br.readLine()) != null) {
			String data[] = tmp.split(",|\\n");
			for (String str : data) {
				custList.add(Integer.parseInt(str));
			}
			List<Integer> actionList = custList.subList(2, custList.size());
			writeCSV(actionList, custList.get(0), custList.get(1));	
			custList.clear();
		}
		br.close();
	}
}
