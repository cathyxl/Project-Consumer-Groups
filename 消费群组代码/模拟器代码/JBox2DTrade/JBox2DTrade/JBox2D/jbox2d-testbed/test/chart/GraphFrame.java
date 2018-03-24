package chart;

import java.awt.GridLayout;
import java.io.IOException;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import model.Aggregation;

public class GraphFrame extends JFrame {
	public GraphFrame() {
		System.out.println(Aggregation.AGGRE_CRITICAL_VALUE);
		try {
			this.setLayout(new GridLayout(2, 2));
			// this.add(new PeopleNumChart().getChartPanel());
//			this.add(new RadiusChart().getChartPanel());
			 this.add(new TimeChart().getChartPanel());
			// this.add(new CheckTimeChart().getChartPanel());
			// // this.add(new SpeedChart().getChartPanel());
			// this.add(new FrequencyChart().getChartPanel());
			this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			this.pack();
			this.setVisible(true);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void main(String args[]) {
		SwingUtilities.invokeLater(new Runnable() {

			@Override
			public void run() {
				// TODO Auto-generated method stub
				new GraphFrame();
			}

		});
	}
}
