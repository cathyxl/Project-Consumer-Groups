package chart;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import javax.swing.JFrame;

import org.jbox2d.common.Vec2;

public class SimilarChart {
	public static final List<R> list = Arrays.asList(//
			new R(new Vec2(-50, 90), new Vec2(-20, 100)), // 1
			new R(new Vec2(-20, 90), new Vec2(10, 100)), // 2
			new R(new Vec2(10, 90), new Vec2(40, 100)), // 3
			new R(new Vec2(40, 70), new Vec2(50, 100)), // 4
			new R(new Vec2(40, 40), new Vec2(50, 70)), // 5
			new R(new Vec2(40, 10), new Vec2(50, 40)), // 6
			new R(new Vec2(20, 0), new Vec2(50, 10)), // 7
			new R(new Vec2(-10, 0), new Vec2(20, 10)), // 8
			new R(new Vec2(-40, 0), new Vec2(-10, 10)), // 9
			new R(new Vec2(-50, 0), new Vec2(-40, 30)), // 10
			new R(new Vec2(-50, 30), new Vec2(-40, 60)),// 11
			new R(new Vec2(-50, 60), new Vec2(-40, 90))// 12
			);

	public static Map<Number, Number> ww(int x, int y) throws IOException {
		int min = Math.min(x, y);
		int max = Math.max(x, y);
		Map<Number, Number> m = new LinkedHashMap<Number, Number>();
		BufferedReader br_score = new BufferedReader(
				new FileReader("score.txt"));
		BufferedReader br_path = new BufferedReader(new FileReader("path.txt"));

		String str;
		Map<String, Number> pg0 = new LinkedHashMap<String, Number>();
		Map<String, Number> pg1 = new LinkedHashMap<String, Number>();

		int count = 0;
		while (count != min && (str = br_score.readLine()) != null) {
			if (str.trim().equals(""))
				count++;
		}
		while ((str = br_score.readLine()) != null && !str.trim().equals("")) {
			if (str.split(" ").length == 1) {
				continue;
			}
			pg0.put(str.split(" ")[0], Integer.parseInt(str.split(" ")[1]));
		}
		count++;
		if (min == max)
			pg1 = pg0;
		else {
			while (count != max && (str = br_score.readLine()) != null) {
				if (str.trim().equals(""))
					count++;
			}
			while ((str = br_score.readLine()) != null
					&& !str.trim().equals("")) {
				if (str.split(" ").length == 1) {
					continue;
				}
				pg1.put(str.split(" ")[0], Integer.parseInt(str.split(" ")[1]));
			}
		}

		// 人数相似度
		float similar_pnum = Math.min(pg0.size(), pg1.size())
				/ Math.max(pg0.size(), pg1.size());
		// 得分相似度
		float score0 = 0;
		float score1 = 0;
		for (Number num : pg0.values()) {
			score0 += num.floatValue();
		}
		score0 = score0 / pg0.size();
		for (Number num : pg1.values()) {
			score1 += num.floatValue();
		}
		score1 = score1 / pg1.size();
		float similar_score = Math.max(score0, score1) == 0 ? 0 : Math.min(
				score0, score1) / Math.max(score0, score1);

		int step = 0;
		int[] mark0 = new int[list.size()];
		int[] mark1 = new int[list.size()];
		while ((str = br_path.readLine()) != null) {
			if (str.trim().equals("")) {
				step++;
				int all = 0;
				int same = 0;
				int sum0 = 0;
				int sum1 = 0;
				for (int i = 0; i < mark1.length; i++) {
					sum0 += mark0[i];
					sum1 += mark1[i];
					if (mark0[i] != 0 || mark1[i] != 0)
						all++;
					if (mark0[i] != 0 && mark1[i] != 0)
						same++;
				}
				// 路径相似性
				float similar_path = all == 0 ? 0 : same / (all + 0.0f);

				float re0 = (sum0 + 0.0f) / step / pg0.size();
				float re1 = (sum1 + 0.0f) / step / pg1.size();
				// 平均停留时间。
				float similar_remain = Math.max(re0, re1) == 0 ? 0 : Math.min(
						re0, re1) / Math.max(re0, re1);
				System.out.println(re0);
				System.out.println(re1);
				System.out.println("&&&&&&&&&&&&");
				m.put(step, (similar_path * 0.1 + similar_pnum * 0.5
						+ similar_remain * 0.3 + similar_score * 0.1));
				continue;
			}
			String[] s = str.split(" ");
			if (pg0.containsKey(s[0])) {
				for (int i = 0; i < list.size(); i++) {
					R r = list.get(i);
					Vec2 v = new Vec2(Float.parseFloat(s[1]),
							Float.parseFloat(s[2]));
					if (r.in(v)) {
						mark0[i]++;
					}
				}
			} else if (pg1.containsKey(s[0])) {
				for (int i = 0; i < list.size(); i++) {
					R r = list.get(i);
					Vec2 v = new Vec2(Float.parseFloat(s[1]),
							Float.parseFloat(s[2]));
					if (r.in(v)) {
						mark1[i]++;
					}
				}
			}
		}

		for (int i = 0; i < mark1.length; i++) {
			System.out.println(mark0[i] + " " + mark1[i]);
		}
		br_score.close();
		br_path.close();
		return m;
	}

	public static void pp(Map<Number, Number> m, String filename)
			throws IOException {
		StringBuffer sbx = new StringBuffer();
		sbx.append("x=[");
		StringBuffer sby = new StringBuffer();
		sby.append("y=[");
		PrintWriter pw = new PrintWriter(filename);
		for (Entry<Number, Number> e : m.entrySet()) {
			System.out.println("***"+e.getKey());
			sbx.append(e.getKey().intValue() + " ");
			sby.append(e.getValue().floatValue() + " ");
		}
		sbx.append("]");
		sby.append("]");
		System.out.println(sbx.length());
		pw.println(sbx.toString());
		pw.println(sby.toString());
		pw.close();
	}

	public static void main(String[] args) throws IOException {
		JFrame jf = new JFrame();
		jf.setSize(500, 500);
		jf.setLocationRelativeTo(null);
		Map<String, Map<Number, Number>> map = new HashMap<String, Map<Number, Number>>();
		Map<Number, Number> m = SimilarChart.ww(7, 13);
		Map<Number, Number> m1 = SimilarChart.ww(7, 19);
		Map<Number, Number> m2 = SimilarChart.ww(7, 31);
		Map<Number, Number> m3 = SimilarChart.ww(7, 41);
		Map<Number, Number> m4 = SimilarChart.ww(7, 48);

		pp(m, "G0_G1");
		pp(m1, "G0_G2");
		pp(m2, "G0_G4");
		pp(m3, "G0_G6");
		pp(m4, "G0_G8");
		map.put("G0-G1", m);
		map.put("G0-G2", m1);
		map.put("G0-G4", m2);
		map.put("G0-G6", m3);
		map.put("G0-G8", m4);
		jf.add(new XYLineChart("title", "categoryAxisLabel", "valueAxisLabel",
				map).chartpanel);
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);

	}

}

class R {
	public Vec2 left;
	public Vec2 right;

	public R(Vec2 left, Vec2 right) {
		super();
		this.left = left;
		this.right = right;
	}

	public boolean in(Vec2 v) {
		if ((left.x - v.x) * (right.x - v.x) < 0
				&& (left.y - v.y) * (right.y - v.y) < 0) {
			return true;
		}
		return false;
	}
}
