package chart;

import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import javax.swing.JFrame;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

public class XYLineChart {
	public ChartPanel chartpanel;

	public XYLineChart(String title, String categoryAxisLabel,
			String valueAxisLabel, Map<String, Map<Number, Number>> map) {
		XYSeriesCollection dataset = createDateset(map);
		JFreeChart chart = ChartFactory.createXYLineChart(title,
				categoryAxisLabel, valueAxisLabel, dataset);
		chart.getTitle().setFont(new Font("隶书", Font.BOLD, 25));
		chart.getLegend().setItemFont(new Font("隶书", Font.BOLD, 15));

		XYPlot xyPlot = chart.getXYPlot();

		ValueAxis domainAxis = xyPlot.getDomainAxis();
		domainAxis.setLabelFont(new Font("隶书", Font.BOLD, 20));
		domainAxis.setTickLabelFont(new Font("隶书", Font.BOLD, 15));

		ValueAxis valueAxis = xyPlot.getRangeAxis();
		valueAxis.setLabelFont(new Font("隶书", Font.BOLD, 20));
		valueAxis.setTickLabelFont(new Font("隶书", Font.BOLD, 15));
		valueAxis.setUpperBound(0.6);

		chartpanel = new ChartPanel(chart);
	}

	private XYSeriesCollection createDateset(
			Map<String, Map<Number, Number>> map) {
		XYSeriesCollection dataset = new XYSeriesCollection();
		for (Entry<String, Map<Number, Number>> entry : map.entrySet()) {
			XYSeries dataSeries = new XYSeries(entry.getKey());
			for (Entry<Number, Number> e : entry.getValue().entrySet()) {
				dataSeries.add(e.getKey(), e.getValue());
			}
			dataset.addSeries(dataSeries);
		}
		return dataset;
	}

	public static void main(String[] args) throws IOException {
		JFrame jf = new JFrame();
		jf.setSize(500, 500);
		jf.setLocationRelativeTo(null);
		jf.setLayout(new GridLayout(3, 4));
		for (int i = 0; i < 12; i++) {
			Map<String, Map<Number, Number>> map = new HashMap<String, Map<Number, Number>>();
			BufferedReader br = new BufferedReader(new FileReader("aggre.txt"));
			String line;
			Map<Number, Number> m0 = new HashMap<Number, Number>();
			Map<Number, Number> m1 = new HashMap<Number, Number>();
			int count = 0;
			while ((line = br.readLine()) != null) {
				count++;
				String[] s = line.split(" ");
				String[] str = s[i].split(",");
				if (str[0].equals("0"))
					m0.put(count, Float.parseFloat(str[2]));
				else if (str[0].equals("1"))
					m1.put(count, Float.parseFloat(str[2]));
			}
			br.close();
			map.put("未宣传", m0);
			map.put("宣传", m1);
			jf.add(new XYLineChart("title"+(i+1), "categoryAxisLabel", "valueAxisLabel",
					map).chartpanel);
			System.out.println(i);
		}
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
	}
}
