"""
路线动线地图生成器
用法：python3 generate_route_map.py
输出：assets/maps/ 目录下的 HTML 文件，用浏览器打开后截图
"""

import folium
import math
import os

# ─────────────────────────────────────────────
# 工具函数：计算两点距离（米）
# ─────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def fmt_dist(meters):
    return f"{meters}m" if meters < 1000 else f"{meters/1000:.1f}km"


# ─────────────────────────────────────────────
# 路线数据（按游览顺序填写）
# 每个打卡点：name / coords / emoji / 交通说明（到下一站）
# ─────────────────────────────────────────────
ROUTES = {
    "清迈Day1：古城→双龙寺→尼曼路": {
        "center": [18.796, 98.970],
        "zoom": 13,
        "waypoints": [
            {
                "name": "①古城东门\n帕兰门",
                "coords": [18.7883, 98.9942],
                "color": "#E53E3E",
                "to_next": {"walk": "步行 10min", "bike": "骑车 5min"},
            },
            {
                "name": "②三王纪念碑",
                "coords": [18.7882, 98.9883],
                "color": "#E53E3E",
                "to_next": {"walk": "步行 3min"},
            },
            {
                "name": "③柴迪隆寺",
                "coords": [18.7873, 98.9877],
                "color": "#E53E3E",
                "to_next": {"walk": "步行 5min"},
            },
            {
                "name": "④帕辛寺",
                "coords": [18.7877, 98.9837],
                "color": "#E53E3E",
                "to_next": {
                    "songthaew": "双条车 30-40min｜60-80铢/人",
                    "motorbike": "摩托出租 30min｜150铢",
                },
            },
            {
                "name": "⑤双龙寺\n素帖山",
                "coords": [18.8048, 98.9218],
                "color": "#C05621",
                "to_next": {
                    "songthaew": "双条车回城 40min｜40-60铢",
                    "grab": "Grab 直达尼曼 30min｜80-100铢",
                },
            },
            {
                "name": "⑥尼曼路\n夜市",
                "coords": [18.7966, 98.9670],
                "color": "#2B6CB0",
                "to_next": None,
            },
        ],
    }
}


# ─────────────────────────────────────────────
# 生成地图
# ─────────────────────────────────────────────
def build_map(title, config):
    m = folium.Map(
        location=config["center"],
        zoom_start=config["zoom"],
        tiles="CartoDB positron",
    )

    waypoints = config["waypoints"]

    for i, wp in enumerate(waypoints):
        lat, lon = wp["coords"]

        # 定位 pin（圆形数字标记）
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background:{wp['color']};
                    color:white;
                    border-radius:50%;
                    width:32px;height:32px;
                    display:flex;align-items:center;justify-content:center;
                    font-weight:bold;font-size:13px;
                    border:2px solid white;
                    box-shadow:0 2px 4px rgba(0,0,0,0.4);
                ">{i+1}</div>""",
                icon_size=(32, 32),
                icon_anchor=(16, 16),
            ),
        ).add_to(m)

        # 名称标签
        label = wp["name"].replace("\n", "<br>")
        folium.Marker(
            location=[lat + 0.003, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background:{wp['color']};
                    color:white;
                    padding:3px 7px;
                    border-radius:6px;
                    font-size:12px;font-weight:bold;
                    white-space:nowrap;
                    box-shadow:0 1px 3px rgba(0,0,0,0.3);
                ">{label}</div>""",
                icon_size=(120, 40),
                icon_anchor=(60, 40),
            ),
        ).add_to(m)

        # 路线箭头 + 距离标注
        if i < len(waypoints) - 1:
            next_wp = waypoints[i + 1]
            nlat, nlon = next_wp["coords"]
            dist = haversine(lat, lon, nlat, nlon)

            # 虚线路线
            folium.PolyLine(
                locations=[[lat, lon], [nlat, nlon]],
                color=wp["color"],
                weight=2.5,
                dash_array="8 5",
                opacity=0.85,
            ).add_to(m)

            # 中点距离标签
            mlat, mlon = (lat + nlat) / 2, (lon + nlon) / 2
            transport_info = ""
            if wp.get("to_next"):
                lines = [f"🚶 {v}" if "步行" in k else f"🚌 {v}" if "songthaew" in k else f"🏍 {v}" if "moto" in k else f"🚗 {v}"
                         for k, v in wp["to_next"].items()]
                transport_info = "<br>".join(lines)

            folium.Marker(
                location=[mlat, mlon],
                icon=folium.DivIcon(
                    html=f"""
                    <div style="
                        background:white;
                        border:1.5px solid {wp['color']};
                        border-radius:8px;
                        padding:3px 8px;
                        font-size:11px;
                        color:#333;
                        white-space:nowrap;
                        box-shadow:0 1px 3px rgba(0,0,0,0.2);
                        text-align:center;
                    ">
                        <b style="color:{wp['color']}">{fmt_dist(dist)}</b>
                        {"<br><span style='color:#555;font-size:10px;'>" + transport_info + "</span>" if transport_info else ""}
                    </div>""",
                    icon_size=(160, 60),
                    icon_anchor=(80, 30),
                ),
            ).add_to(m)

    # 标题
    title_html = f"""
    <div style="
        position:fixed;top:10px;left:50%;transform:translateX(-50%);
        background:#E53E3E;color:white;
        padding:8px 20px;border-radius:20px;
        font-size:16px;font-weight:bold;
        z-index:9999;box-shadow:0 2px 6px rgba(0,0,0,0.3);
    ">{title}</div>"""
    m.get_root().html.add_child(folium.Element(title_html))

    return m


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "maps")
    os.makedirs(out_dir, exist_ok=True)

    for title, config in ROUTES.items():
        safe_name = title.replace("：", "-").replace("/", "-").replace(" ", "_")
        out_path = os.path.join(out_dir, f"{safe_name}.html")
        m = build_map(title, config)
        m.save(out_path)
        print(f"✅ 已生成：{out_path}")

    print("\n👉 用浏览器打开 HTML 文件，调整缩放后截图即可")
    print("   建议截图尺寸：1080x1920（9:16 竖版，适合小红书）")
