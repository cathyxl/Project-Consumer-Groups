package chart;

import io.FileIO;

import java.awt.Font;
import java.io.IOException;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.data.category.DefaultCategoryDataset;

public class SpeedChart {
	ChartPanel frame1;

	public SpeedChart() throws IOException {
		DefaultCategoryDataset xydataset = createDataset();
		JFreeChart jfreechart = ChartFactory.createLineChart("SpeedChart",
				"Speed of people", "Number", xydataset);
		frame1 = new ChartPanel(jfreechart, true);
		jfreechart.getLegend().setItemFont(new Font("黑体", Font.BOLD, 15));
		jfreechart.getTitle().setFont(new Font("宋体", Font.BOLD, 20));// 设置标题字体

	}

	private static DefaultCategoryDataset createDataset() throws IOException { // 这个数据集有点多，但都不难理解
		DefaultCategoryDataset linedataset = new DefaultCategoryDataset();
		// 各曲线名称
		String series1 = "E2T";
		String series2 = "E3T";
		String series3 = "E2T1";
		String series4 = "CMP";
		String series5 = "E3T1";
		String series6 = "MaxPass";
		String series7 = "AveragePass";
		// 横轴名称(列名称)
		String type1 = "10";
		String type2 = "30";
		String type3 = "50";
		String type4 = "70";
		String type5 = "90";
		String type6 = "110";
		String type7 = "130";
		// int x1=FileIO.getTwo("aggre_225_8000_15.txt");
		// int y1=FileIO.getThree("aggre_225_8000_15.txt");
		// int x2=FileIO.getTwo("aggre_100_8000_15.txt");
		// int y2=FileIO.getThree("aggre_100_8000_15.txt");
		// int x3=FileIO.getTwo("aggre_125_8000_15.txt");
		// int y3=FileIO.getThree("aggre_125_8000_15.txt");
		// int x4=FileIO.getTwo("aggre_150_8000_15.txt");
		// int y4=FileIO.getThree("aggre_150_8000_15.txt");
		// int x5=FileIO.getTwo("aggre_175_8000_15.txt");
		// int y5=FileIO.getThree("aggre_175_8000_15.txt");
		// int x6=FileIO.getTwo("aggre_75_8000_15.txt");
		// int y6=FileIO.getThree("aggre_75_8000_15.txt");
		// int x7=FileIO.getTwo("aggre_200_8000_15.txt");
		// int y7=FileIO.getThree("aggre_200_8000_15.txt");

		int x1 = FileIO.getTwoAll("speed/aggre_150_80_15_10", 20);
		// int y1=FileIO.getThreeAll("speed/aggre_150_80_15_10", 20);
		int[] z1 = FileIO.getTwoAll1("speed/shop_150_80_15_10", 20);
		int[] h1 = FileIO.dataCompare("speed", "150_80_15_10");

		int x2 = FileIO.getTwoAll("speed/aggre_150_80_15_30", 20);
		// int y2=FileIO.getThreeAll("speed/aggre_150_80_15_30", 20);
		int[] z2 = FileIO.getTwoAll1("speed/shop_150_80_15_30", 20);
		int[] h2 = FileIO.dataCompare("speed", "150_80_15_30");

		int x3 = FileIO.getTwoAll("speed/aggre_150_80_15_50", 20);
		// int y3=FileIO.getThreeAll("speed/aggre_150_80_15_50", 20);
		int[] z3 = FileIO.getTwoAll1("speed/shop_150_80_15_50", 20);
		int[] h3 = FileIO.dataCompare("speed", "150_80_15_50");

		int x4 = FileIO.getTwoAll("speed/aggre_150_80_15_70", 20);
		// int y4=FileIO.getThreeAll("speed/aggre_150_80_15_70", 20);
		int[] z4 = FileIO.getTwoAll1("speed/shop_150_80_15_70", 20);
		int[] h4 = FileIO.dataCompare("speed", "150_80_15_70");

		int x5 = FileIO.getTwoAll("speed/aggre_150_80_15_90", 20);
		// int y5=FileIO.getThreeAll("speed/aggre_150_80_15_90", 20);
		int[] z5 = FileIO.getTwoAll1("speed/shop_150_80_15_90", 20);
		int[] h5 = FileIO.dataCompare("speed", "150_80_15_90");

		int x6 = FileIO.getTwoAll("speed/aggre_150_80_15_110", 20);
		// int y6=FileIO.getThreeAll("speed/aggre_150_80_15_110", 20);
		int[] z6 = FileIO.getTwoAll1("speed/shop_150_80_15_110", 20);
		int[] h6 = FileIO.dataCompare("speed", "150_80_15_110");

		int x7 = FileIO.getTwoAll("speed/aggre_150_80_15_130", 20);
		// int y7=FileIO.getThreeAll("speed/aggre_150_80_15_130", 20);
		int[] z7 = FileIO.getTwoAll1("speed/shop_150_80_15_130", 20);
		int[] h7 = FileIO.dataCompare("speed", "150_80_15_130");
		linedataset.addValue(x1, series1, type1);
		// linedataset.addValue(y1, series2, type1);
		linedataset.addValue(h1[3], series3, type1);
		linedataset.addValue(h1[0], series4, type1);
		linedataset.addValue(h1[1], series5, type1);
		linedataset.addValue(z1[2], series6, type1);
		linedataset.addValue(z1[1], series7, type1);

		linedataset.addValue(x2, series1, type2);
		// linedataset.addValue(y2, series2, type2);
		linedataset.addValue(h2[3], series3, type2);
		linedataset.addValue(h2[0], series4, type2);
		linedataset.addValue(h2[1], series5, type2);
		linedataset.addValue(z2[2], series6, type2);
		linedataset.addValue(z2[1], series7, type2);

		linedataset.addValue(x3, series1, type3);
		// linedataset.addValue(y3, series2, type3);
		linedataset.addValue(h3[3], series3, type3);
		linedataset.addValue(h3[0], series4, type3);
		linedataset.addValue(h3[1], series5, type3);
		linedataset.addValue(z3[2], series6, type3);
		linedataset.addValue(z3[1], series7, type3);

		linedataset.addValue(x4, series1, type4);
		// linedataset.addValue(y4, series2, type4);
		linedataset.addValue(h4[3], series3, type4);
		linedataset.addValue(h4[0], series4, type4);
		linedataset.addValue(h4[1], series5, type4);
		linedataset.addValue(z4[2], series6, type4);
		linedataset.addValue(z4[1], series7, type4);

		linedataset.addValue(x5, series1, type5);
		// linedataset.addValue(y5, series2, type5);
		linedataset.addValue(h5[3], series3, type5);
		linedataset.addValue(h5[0], series4, type5);
		linedataset.addValue(h5[1], series5, type5);
		linedataset.addValue(z5[2], series6, type5);
		linedataset.addValue(z5[1], series7, type5);

		linedataset.addValue(x6, series1, type6);
		// linedataset.addValue(y6, series2, type6);
		linedataset.addValue(h6[3], series3, type6);
		linedataset.addValue(h6[0], series4, type6);
		linedataset.addValue(h6[1], series5, type6);
		linedataset.addValue(z6[2], series6, type6);
		linedataset.addValue(z6[1], series7, type6);

		linedataset.addValue(x7, series1, type7);
		// linedataset.addValue(y7, series2, type7);
		linedataset.addValue(h7[3], series3, type7);
		linedataset.addValue(h7[0], series4, type7);
		linedataset.addValue(h7[1], series5, type7);
		linedataset.addValue(z7[2], series6, type7);
		linedataset.addValue(z7[1], series7, type7);

		System.out.println("speed");
		System.out.println("E2T=[" + x1 + " " + x2 + " " + x3 + " " + x4 + " "
				+ x5 + " " + x6 + " " + x7 + "]");
		System.out.println("E2T1=[" + h1[3] + " " + h2[3] + " " + h3[3] + " "
				+ h4[3] + " " + h5[3] + " " + h6[3] + " " + h7[3] + "]");
		// System.out.println("E3T=["+y1+" "+y2+" "+y3+" "+y4+" "+y5+" "+y6+" "+y7+"]");
		System.out.println("E3T1=[" + h1[1] + " " + h2[1] + " " + h3[1] + " "
				+ h4[1] + " " + h5[1] + " " + h6[1] + " " + h7[1] + "]");
		System.out.println("CMP=[" + h1[0] + " " + h2[0] + " " + h3[0] + " "
				+ h4[0] + " " + h5[0] + " " + h6[0] + " " + h7[0] + "]");
		System.out.println("MaxPass=[" + z1[2] + " " + z2[2] + " " + z3[2]
				+ " " + z4[2] + " " + z5[2] + " " + z6[2] + " " + z7[2] + "]");
		System.out.println("Average=[" + z1[1] + " " + z2[1] + " " + z3[1]
				+ " " + z1[1] + " " + z5[1] + " " + z6[1] + " " + z7[1] + "]");

		return linedataset;
	}

	public ChartPanel getChartPanel() {
		return frame1;

	}
}
