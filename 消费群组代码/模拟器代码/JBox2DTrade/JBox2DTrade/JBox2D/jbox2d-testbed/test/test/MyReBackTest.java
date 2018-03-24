package test;

import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import model.Mall;
import model.People;

import org.jbox2d.collision.shapes.CircleShape;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;
import org.jbox2d.dynamics.BodyDef;
import org.jbox2d.dynamics.BodyType;
import org.jbox2d.testbed.framework.TestbedSettings;
import org.jbox2d.testbed.framework.TestbedTest;

public class MyReBackTest extends TestbedTest {
	/**
	 * 是否开始实验。
	 */
	public boolean isStart = false;
	public List<Body> people = new ArrayList<Body>();
	public BufferedReader br;

	@Override
	public void initTest(boolean deserialized) {
		if (deserialized)
			return;
		people.clear();
		if (br != null)
			try {
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		Mall mall = Mall.initMall(getWorld());
	}

	/**
	 * 按s键，模拟实验开始,e结束。
	 */
	@Override
	public void keyPressed(char keyChar, int keyCode) {
		super.keyPressed(keyChar, keyCode);
		if (KeyEvent.VK_S == keyCode && !isStart) {
			isStart = true;
			try {
				br = new BufferedReader(new FileReader(SimulationTest.PATH));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		} else if (KeyEvent.VK_E == keyCode && isStart) {
			for (int i = 0; i < people.size(); i++) {
				getWorld().destroyBody(people.get(i));
			}
			people.clear();
		}
	}

	@Override
	public void step(TestbedSettings settings) {
		super.step(settings);
		if (isStart) {
			String str = null;
			try {
				for (int i = 0; i < people.size(); i++) {
					getWorld().destroyBody(people.get(i));
				}
				people.clear();
				while ((str = br.readLine()) != null && !str.equals("")) {
					String[] s = str.split(" ");
					BodyDef peopleDef = new BodyDef();
					peopleDef.linearDamping = 0.0f;
					peopleDef.angularDamping = 1.0f;
					peopleDef.type = BodyType.DYNAMIC;

					peopleDef.position = new Vec2(Float.parseFloat(s[1]),
							Float.parseFloat(s[2]));

					Body p = getWorld().createBody(peopleDef);
					CircleShape peopleShape = new CircleShape();
					peopleShape.setRadius(People.PEOPLE_RADIUS);

					p.createFixture(peopleShape, 3.0f);
					p.setUserData(new People(Integer.parseInt(s[0])));
					people.add(p);
				}
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			if (str == null) {
				isStart = false;
				for (int i = 0; i < people.size(); i++) {
					getWorld().destroyBody(people.get(i));
				}
				people.clear();
			}
		}
	}

	@Override
	public String getTestName() {
		return "重现实验";
	}

}
