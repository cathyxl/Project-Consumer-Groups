package chart;

import java.awt.Font;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeSet;

import javax.swing.JFrame;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.CategoryLabelPositions;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.category.DefaultCategoryDataset;

import util.Tool;

public class BarChart {
	public ChartPanel chartpanel;

	public BarChart(String title, String categoryAxisLabel,
			String valueAxisLabel, Map<String, Map<String, Number>> map) {
		CategoryDataset dataset = createDateset(map);
		JFreeChart chart = ChartFactory.createBarChart3D(title,
				categoryAxisLabel, valueAxisLabel, dataset);
		chart.getTitle().setFont(new Font("隶书", Font.BOLD, 25));
		chart.getLegend().setItemFont(new Font("隶书", Font.BOLD, 20));
		CategoryPlot categoryPlot = chart.getCategoryPlot();
		System.out.println();

		CategoryAxis categoryAxis = categoryPlot.getDomainAxis();
		categoryAxis.setLabelFont(new Font("隶书", Font.BOLD, 20));
		categoryAxis.setTickLabelFont(new Font("隶书", Font.BOLD, 15));
		// categoryAxis.setCategoryLabelPositions(CategoryLabelPositions.UP_45);

		ValueAxis valueAxis = categoryPlot.getRangeAxis();
		valueAxis.setLabelFont(new Font("隶书", Font.BOLD, 20));
		valueAxis.setTickLabelFont(new Font("隶书", Font.BOLD, 15));

		chartpanel = new ChartPanel(chart);
	}

	private CategoryDataset createDateset(Map<String, Map<String, Number>> map) {
		DefaultCategoryDataset dataset = new DefaultCategoryDataset();
		for (Entry<String, Map<String, Number>> e : map.entrySet()) {
			for (Entry<String, Number> entry : e.getValue().entrySet()) {
				dataset.addValue(entry.getValue(),entry.getKey() , "");
			}
		}
		return dataset;
	}

	public static void main(String[] args) {
		JFrame jf = new JFrame();
		jf.setSize(500, 500);
		jf.setLocationRelativeTo(null);
		try {
			BufferedReader br = new BufferedReader(new FileReader("score.txt"));
			String str;
			Map<String, Map<String, Number>> map = new LinkedHashMap<String, Map<String, Number>>();
			Map<String, Map<String, Number>> map0 = new LinkedHashMap<String, Map<String, Number>>();
			int count = 0;
			Map<String, Number> m = null;
			String key = null;
			while ((str = br.readLine()) != null && count < 2) {
				if (str.trim().equals("")) {
					count++;
					if (m.size() == 0)
						continue;
					map.put(key, m);
					continue;
				}
				if (str.split(" ").length == 1) {
					System.out.println("***");
					key = str.trim();
					m = new LinkedHashMap<String, Number>();
					continue;
				}
				if(Integer.parseInt(str.split(" ")[1])!=0||Tool.probility(0.5f))
				m.put(str.split(" ")[0], Integer.parseInt(str.split(" ")[1]));
			}
			Set<Entry<String, Number>> list = new TreeSet<Entry<String, Number>>(
					new MM());
			int yy=0;
			Map<String, Number> mmm = new LinkedHashMap<String, Number>();
			for (Entry<String, Map<String, Number>> e : map.entrySet()) {
				for (Entry<String, Number> entry : e.getValue().entrySet()) {
					mmm.put(yy+"", entry.getValue());
					yy++;
				}
			}
			for (Entry<String, Number> entry : mmm.entrySet()) {
				list.add(entry);
			}
			Map<String, Number> mm = new LinkedHashMap<String, Number>();
			for (Entry<String, Number> entry : list) {
				mm.put(entry.getKey(), entry.getValue());
			}
			map0.put("", mm);
			jf.add(new BarChart("", "member ID", "impact value",
					map0).chartpanel);
			br.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
	}
}

class MM implements Comparator<Entry<String, Number>> {

	@Override
	public int compare(Entry<String, Number> m0, Entry<String, Number> m1) {
		int m = m1.getValue().intValue() - m0.getValue().intValue();
		return m == 0 ? 1 : m;
	}
}
