package ui;

import javax.swing.*;

public class ShowUI extends JFrame{
	public ShowUI(){
		JLinePanel jp=new JLinePanel();
		this.add(jp);
		this.pack();
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setVisible(true);
	}
}
