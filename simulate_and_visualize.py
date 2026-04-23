import math
import csv
import time as time_lib
import os

GRAVITY = -9.80665
AIR_DENSITY = 1.225
PI = math.pi

def simulate():
    # ISA Sabitleri ve RK4 Parametreleri
    RHO_0, T0, L, R, G, SOS_0 = 1.225, 288.15, 0.0065, 287.05, 9.80665, 340.29
    mass, base_cd, area = 43.0, 0.22, 0.018
    wind_z = 10.0
    dt, time, px, py, pz = 0.01, 0.0, 0.0, 0.0, 0.0
    speed, angle_rad = 850.0, 45.0 * math.pi / 180.0
    vx, vy, vz = speed * math.cos(angle_rad), speed * math.sin(angle_rad), 0.0
    
    # HEDEF BİLGİSİ
    target_x, target_y, target_z = 20000.0, 0, 500.0
    
    results = []

    # RK4 Türev Fonksiyonu (Güdüm Destekli)
    def get_accel(p_x, p_y, p_z, v_x, v_y, v_z):
        h = max(0, min(p_y, 11000))
        temp = T0 - L * h
        rho = RHO_0 * math.pow(temp / T0, (G / (R * L)) - 1.0)
        v_rel_x, v_rel_y, v_rel_z = v_x, v_y, v_z - wind_z
        v_mag = math.sqrt(v_rel_x**2 + v_rel_y**2 + v_rel_z**2)
        mach = v_mag / SOS_0
        cd = base_cd * 2.8 if 0.8 < mach < 1.2 else (base_cd * 1.5 if mach >= 1.2 else base_cd)
        
        # Aerodinamik Sürükleme
        drag_mag = 0.5 * rho * (v_mag**2) * cd * area if v_mag > 0 else 0
        ax_drag = -(drag_mag * (v_rel_x / v_mag)) / mass if v_mag > 0 else 0
        ay_drag = -G - (drag_mag * (v_rel_y / v_mag)) / mass if v_mag > 0 else -G
        az_drag = -(drag_mag * (v_rel_z / v_mag)) / mass if v_mag > 0 else 0

        # GÜDÜM (Proportional Navigation)
        rel_pos_x, rel_pos_y, rel_pos_z = target_x - p_x, target_y - p_y, target_z - p_z
        dist = math.sqrt(rel_pos_x**2 + rel_pos_y**2 + rel_pos_z**2)
        if dist > 10:
            los_x, los_y, los_z = rel_pos_x/dist, rel_pos_y/dist, rel_pos_z/dist
            v_curr_mag = math.sqrt(v_x**2 + v_y**2 + v_z**2)
            g_dir_x, g_dir_y, g_dir_z = los_x*3.0 - v_x/v_curr_mag, los_y*3.0 - v_y/v_curr_mag, los_z*3.0 - v_z/v_curr_mag
            ax_g, ay_g, az_g = g_dir_x * v_curr_mag * 0.4, g_dir_y * v_curr_mag * 0.4, g_dir_z * v_curr_mag * 0.4
            
            # G-Limit (5G)
            g_mag = math.sqrt(ax_g**2 + ay_g**2 + az_g**2)
            if g_mag > 5*G:
                scale = (5*G)/g_mag
                ax_g, ay_g, az_g = ax_g*scale, ay_g*scale, az_g*scale
        else:
            ax_g, ay_g, az_g = 0, 0, 0

        return (ax_drag + ax_g, ay_drag + ay_g, az_drag + az_g, rho, mach, 0.5 * rho * v_mag**2)

    while py >= 0:
        ax, ay, az, rho, mach, q = get_accel(px, py, pz, vx, vy, vz)
        results.append([time, px, py, pz, math.sqrt(vx**2 + vy**2 + vz**2), rho, mach, q])
        
        # RK4 Adımı
        k1_vx, k1_vy, k1_vz, _, _, _ = get_accel(px, py, pz, vx, vy, vz)
        k2_vx, k2_vy, k2_vz, _, _, _ = get_accel(px + vx*dt*0.5, py + vy*dt*0.5, pz + vz*dt*0.5, vx + k1_vx*dt*0.5, vy + k1_vy*dt*0.5, vz + k1_vz*dt*0.5)
        k3_vx, k3_vy, k3_vz, _, _, _ = get_accel(px + vx*dt*0.5, py + vy*dt*0.5, pz + vz*dt*0.5, vx + k2_vx*dt*0.5, vy + k2_vy*dt*0.5, vz + k2_vz*dt*0.5)
        k4_vx, k4_vy, k4_vz, _, _, _ = get_accel(px + vx*dt, py + vy*dt, pz + vz*dt, vx + k3_vx*dt, vy + k3_vy*dt, vz + k3_vz*dt)

        vx += (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx) * (dt / 6.0)
        vy += (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy) * (dt / 6.0)
        vz += (k1_vz + 2*k2_vz + 2*k3_vz + k4_vz) * (dt / 6.0)
        px, py, pz = px + vx * dt, py + vy * dt, pz + vz * dt
        time += dt
        if time > 500: break

    with open('trajectory_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'X', 'Y', 'Z', 'Velocity', 'Density', 'Mach', 'DynamicPressure'])
        writer.writerows(results)

    # --- HTML GÜNCELLEME BÖLÜMÜ ---
    print("\nHTML Paneli güncelleniyor...")
    
    # Grafikte çok fazla nokta olmasın diye veriyi seyrelt (Örn: her 50 noktadan biri)
    chart_data_x = [round(r[1], 1) for r in results[::50]]
    chart_data_y = [round(r[2], 1) for r in results[::50]]
    chart_data_z = [round(r[3], 1) for r in results[::50]]

    metrics = {
        "max_range": f"{px:,.0f} m",
        "flight_time": f"{time:.1f} s",
        "z_drift": f"{pz:.1f} m",
        "terminal_vel": f"{results[-1][4]:.1f} m/s",
        "min_rho": f"{min(r[5] for r in results):.3f} kg/m3",
        "max_mach": f"{max(r[6] for r in results):.2f}",
        "max_q": f"{max(r[7] for r in results)/1000:.1f} kPa"
    }

    try:
        import os
        target_html = r"C:\Users\kapta\roketsan\index.html"
        
        if not os.path.exists(target_html):
            print(f"HATA: Hedef dosya bulunamadı: {target_html}")
            return

        with open(target_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

        print(f"ASTRA DEBUG: {len(chart_data_x)} veri noktası hazırlandı.")

        # Minimalist yapı için işaretçiler (PLACE_HOLDER olarak güncellendi)
        start_marker = "// --- DATA_PLACE_HOLDER ---"
        end_marker = "// --- DATA_PLACE_HOLDER_END ---"
        
        if start_marker in html_content and end_marker in html_content:
            parts = html_content.split(start_marker)
            rest = parts[1].split(end_marker)
            
            data_js = (f"\n        const xDataFull = {chart_data_x};\n"
                       f"        const yDataFull = {chart_data_y};\n"
                       f"        const zDataFull = {chart_data_z};\n        ")
            
            new_content = parts[0] + start_marker + data_js + end_marker + rest[1]
            
            # Metrikleri yerleştir (Yeni minimalist ID'ler)
            new_content = new_content.replace('id="val-cep" style="color: var(--danger);">--', f'id="val-cep" style="color: var(--danger);">{metrics["z_drift"]}')
            new_content = new_content.replace('id="val-time">--', f'id="val-time">{metrics["flight_time"]}')
            new_content = new_content.replace('id="val-alt">--', f'id="val-alt">{max(chart_data_y) if chart_data_y else 0} m')
            new_content = new_content.replace('id="val-vel">--', f'id="val-vel">{metrics["terminal_vel"]}')

            with open(target_html, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"ASTRA SYSTEMS: {target_html} başarıyla güncellendi.")
        else:
            print("HATA: İşaretçiler (markers) bulunamadı!")
    except Exception as e:
        print(f"HATA: {e}")

    # Animasyon (Opsiyonel - istersen burayı kapatabilirsin)
    # ... (mevcut animasyon kodu buraya gelecek)

if __name__ == "__main__":
    simulate()
