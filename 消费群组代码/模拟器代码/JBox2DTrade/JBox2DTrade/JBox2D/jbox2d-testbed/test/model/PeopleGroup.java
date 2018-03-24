package model;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.jbox2d.common.MathUtils;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;

public class PeopleGroup {
	/**
	 * PeopleGroup以master为中心的半径。
	 */
	public static final float RADIUS = 5f;
	public float attract = 0.49f;
	public int id;
	public int number = 0;// 每组人数
	public Body master;
	public int PatShop;
	public int PatLastShop;
	public List<Body> others = new ArrayList<Body>();
	public Map<Body, Integer> score = new LinkedHashMap<Body, Integer>();

	public PeopleGroup() {
	}

	public PeopleGroup(int id, Body master, List<Body> others) {
		super();
		this.id = id;
		this.master = master;
		this.number++;
		this.PatShop = -1;
		this.PatLastShop = -1;
		score.put(master, 0);
		this.others.addAll(others);
		for (int i = 0; i < this.others.size(); i++) {
			score.put(this.others.get(i), 0);
			this.others.get(i).pgNo = id;
			this.number++;
		}

	}

	/**
	 * 维持PeopleGroup里人员与master不超过RADIUS。若超过，则给予他往master方向的速度,速度大小walk_speed(
	 * master被吸引，则速度为attract_speed) .,若小于People. PEOPLE_RADIUS+0.1f， 则给予随机速度。
	 * 若master或others速度为0， 则给予随机速度。
	 */
	public void maintain() {
		if (master.getLinearVelocity().length() == 0)
			master.setLinearVelocity(People.randomNormalSpeed());
		for (int i = 0; i < others.size(); i++) {
			Body b = others.get(i);
			float distance = MathUtils.distance(b.getPosition(),
					master.getPosition());
			if (distance >= RADIUS) {
				Vec2 v = master.getPosition().sub(b.getPosition());
				if (((People) master.getUserData()).isAttract)
					b.setLinearVelocity(v.mul(((People) b.getUserData()).attract_speed
							/ distance));
				else
					b.setLinearVelocity(v.mul(((People) b.getUserData()).walk_speed
							/ distance));
			} else if (distance < People.PEOPLE_RADIUS + 0.1f)
				b.setLinearVelocity(People.randomNormalSpeed());
		}
	}

	/**
	 * 初始化分数。
	 */
	public void initScore() {
		for (Body b : score.keySet()) {
			score.put(b, 0);
		}
	}
}
