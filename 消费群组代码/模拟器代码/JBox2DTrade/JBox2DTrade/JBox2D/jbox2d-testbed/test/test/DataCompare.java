package test;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

public class DataCompare {

	public static void main(String args[]) {
		// 插入R中的代码
		// try {
		// RConnection c = new RConnection();
		// REXP x = c.eval("R.version.string");
		// System.out.println(x.asString());
		// System.out.println("connected!");
		// String fileName =
		// "C:\\Users\\a\\Desktop\\JBox2DTrade\\JBox2D\\jbox2d-testbed\\frequency\\positionclust.r";
		// c.assign("fileName", fileName);
		// c.eval("source(fileName)");
		// c.close();
		// } catch (RserveException e) {
		// // TODO Auto-generated catch block
		// e.printStackTrace();
		// }
		ClassifyGroup classifyGroup = new ClassifyGroup();
		classifyGroup
				.start("C:\\Users\\a\\Desktop\\JBox2DTrade\\JBox2D\\jbox2d-testbed\\frequency\\adjacency.txt");
		classifyGroup.printGroupList();
		GroupIDReader groupIDReader = new GroupIDReader();
		groupIDReader
				.read("C:\\Users\\a\\Desktop\\JBox2DTrade\\JBox2D\\jbox2d-testbed\\frequency\\groupid.txt");
		groupIDReader.printGroupList();
		System.out.println(groupIDReader.calculateAccuracy(
				groupIDReader.getGroupList(), classifyGroup.getGroupList()));
	}
}

class GroupIDReader {
	private String inputString;
	private String curLine;
	private final ArrayList<ArrayList<String>> groupList = new ArrayList<ArrayList<String>>();

	public ArrayList<ArrayList<String>> getGroupList() {
		return groupList;
	}

	public void read(String fileName) {
		try {
			File file = new File(fileName);
			FileInputStream fileIn = new FileInputStream(file);
			int size = fileIn.available();
			byte[] buffer = new byte[size];
			fileIn.read(buffer);
			fileIn.close();
			inputString = new String(buffer, "UTF-8");
		} catch (FileNotFoundException e) {
			System.out.println(" File " + fileName + " not found.");
			return;
		} catch (IOException e) {
			e.printStackTrace();
			return;
		}
		int newlineSymbolPos;
		while ((newlineSymbolPos = inputString.indexOf('\n')) != -1) {
			curLine = inputString.substring(0, newlineSymbolPos - 1);
			inputString = inputString.substring(newlineSymbolPos + 1);
			addIntoGroupList(curLine);
		}
	}

	private void addIntoGroupList(String lineString) {
		int pid;
		int gid;
		ArrayList<String> group = new ArrayList<String>();
		String[] idWithGroup = lineString.split(" ");
		pid = Integer.parseInt(idWithGroup[0]);
		gid = Integer.parseInt(idWithGroup[1]);
		if (gid > groupList.size() - 1) {
			group.add(pid + "");
			groupList.add(group);
		} else {
			groupList.get(gid).add(pid + "");
		}
	}

	public void printGroupList() {
		int i = 0;
		for (ArrayList<String> group : groupList) {
			// if(group.size()>=2){
			System.out.print(i + ": ");
			for (String peopleID : group) {
				System.out.print(peopleID + " ");
			}
			System.out.println();
			// }
			i++;
		}
	}

	public double calculateAccuracy(ArrayList<ArrayList<String>> origin,
			ArrayList<resultGroup> result) {
		int hits = 0;

		for (ArrayList<String> originGroup : origin) {
			for (int i = 0; i < originGroup.size(); i++) {
				String p = originGroup.get(i);
				inner: for (resultGroup re : result) {
					if (re.reGroup.contains(p)) {
						re.count++;
						if (re.count / originGroup.size() >= 0.8 && !re.b) {
							hits++;
							re.b = true;
						} else {
							break inner;
						}
					}
				}
			}
		}

		System.out.println(hits);
		System.out.println(origin.size());
		return (double) hits / (double) origin.size();
	}
}

class ClassifyGroup {
	private String inputString;
	private String curLine;
	private int lineNum = 1;
	private final ArrayList<resultGroup> groupList;

	public ClassifyGroup() {
		groupList = new ArrayList<resultGroup>();
	}

	public void start(String fileName) {
		try {
			File file = new File(fileName);
			FileInputStream fileIn = new FileInputStream(file);
			int size = fileIn.available();
			byte[] buffer = new byte[size];
			fileIn.read(buffer);
			fileIn.close();
			inputString = new String(buffer, "UTF-8");
		} catch (FileNotFoundException e) {
			System.out.println("File " + fileName + " not found.");
			return;
		} catch (IOException e) {
			e.printStackTrace();
			return;
		}
		int newlineSymbolPos;
		while ((newlineSymbolPos = inputString.indexOf('\n')) != -1) {
			curLine = inputString.substring(0, newlineSymbolPos);
			inputString = inputString.substring(newlineSymbolPos + 1);
			analyzeSingleLine(curLine);
			lineNum++;
		}
	}

	private void analyzeSingleLine(String lineString) {
		double relevancy;// 相关度
		String[] releList = lineString.split(" ");
		boolean needNewGroup = true;// 是否增加新组
		resultGroup temporaryGroup = new resultGroup();
		_FOR_01_: for (resultGroup re : groupList) {
			for (String peopleID : re.getReGroup()) {
				if (lineNum == Integer.parseInt(peopleID)) {
					needNewGroup = false;
					temporaryGroup = re;
					break _FOR_01_;
				}
			}
		}

		//
		if (needNewGroup) {
			_FOR_02_: for (int i = lineNum - 1, columnNum = lineNum; i < releList.length; i++) {
				relevancy = Double.parseDouble(releList[i]);
				if (relevancy >= 100) {
					for (resultGroup re : groupList) {
						for (String peopleID : re.getReGroup()) {
							if (columnNum == Integer.parseInt(peopleID)) {
								temporaryGroup = re;
								temporaryGroup.getReGroup().add(lineNum + "");
								needNewGroup = false;
								break _FOR_02_;
							}
						}
					}
				}
				columnNum++;
			}
		}

		if (needNewGroup) {

			temporaryGroup.getReGroup().add(lineNum + "");
		}
		for (int i = lineNum - 1, columnNum = lineNum; i < releList.length; i++) {
			relevancy = Double.parseDouble(releList[i]);
			if (relevancy >= 5) {
				boolean isExisting = false;
				for (String peopleID : temporaryGroup.reGroup) {
					if (columnNum == Integer.parseInt(peopleID)) {
						isExisting = true;
						break;
					}
				}
				if (!isExisting)
					temporaryGroup.reGroup.add(columnNum + "");
			}
			columnNum++;
		}

		if (needNewGroup)
			groupList.add(temporaryGroup);
	}

	public void printGroupList() {
		int i = 0;
		for (resultGroup re : groupList) {
			// if(group.size()>=2){
			System.out.print(i + ": ");
			for (String peopleID : re.reGroup) {
				System.out.print(peopleID + " ");
			}
			System.out.println();
			// }
			i++;
		}
	}

	public ArrayList<resultGroup> getGroupList() {
		return groupList;
	}
}