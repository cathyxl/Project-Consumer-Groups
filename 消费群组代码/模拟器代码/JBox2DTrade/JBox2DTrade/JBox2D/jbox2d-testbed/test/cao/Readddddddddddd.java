package cao;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class Readddddddddddd {

	public static void main(String[] args) throws IOException {
		PrintWriter pw = new PrintWriter("data");
		BufferedReader br = new BufferedReader(new FileReader("G0_G1"));
		String s = br.readLine();
		String ss[] = s.substring(3, s.length() - 1).trim().split(" ");
		StringBuffer sb = new StringBuffer();
		for (int i = 0; i < 10000; i++) {
			sb.append(ss[i] + " ");
		}
		pw.println("x=[" + sb.toString() + "]");
		br.close();
		nnn("G0_G1", pw);
		nnn("G0_G2", pw);
		nnn("G0_G4", pw);
		nnn("G0_G6", pw);
		nnn("G0_G8", pw);
		nnn("G1_G2", pw);
		nnn("G3_G4", pw);
		nnn("G5_G6", pw);
		nnn("G7_G8", pw);
		pw.close();
	}

	public static void nnn(String ff, PrintWriter pw) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(ff));
		br.readLine();
		String s=br.readLine();
		String ss[] = s.substring(3, s.length() - 1).trim().split(" ");
		StringBuffer sb = new StringBuffer();
		for (int i = 0; i < 10000; i++) {
			sb.append(ss[i] + " ");
		}
		pw.println(ff+"=[" + sb.toString() + "]");
		pw.flush();
		br.close();
	}

}
