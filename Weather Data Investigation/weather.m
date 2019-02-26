clear all; clc;
ncfile = 'james.nc';
load coastlines

% ncdisp(ncfile)
WM_LONG = -28.1767682;
WM_LAT = 149.6498806;
LATLONG_STEP = 0.05; % step size (deg)
LAT_DIST = 5 * LATLONG_STEP;
LONG_DIST = 5 * LATLONG_STEP;

WESTMAR_LONG = [WM_LONG - LONG_DIST, WM_LONG + LONG_DIST];
WESTMAR_LAT = [WM_LAT - LAT_DIST, WM_LAT + LAT_DIST];

longitude = ncread(ncfile, 'lon');
latitude = ncread(ncfile, 'lat');
ridge = ncread(ncfile, 'ridge');
cape = ncread(ncfile, 'cape');
vel_u = ncread(ncfile, 'U');
vel_v = ncread(ncfile, 'V');
vel_w = ncread(ncfile, 'W');
vel_total = (vel_u.^2 + vel_v.^2 + vel_w.^2).^0.5;
surf_temp = ncread(ncfile, 'sfctemp');

long_max = max(longitude);
long_min = min(longitude);
lat_max = max(latitude);
lat_min = min(latitude);
long_range = long_max - long_min;
lat_range = lat_max -lat_min;
long_step = long_range/length(longitude);
lat_step = lat_range/length(latitude);

WM_DLONG = abs(WM_LONG - long_min)/long_step;
WM_DLAT = abs(WM_LAT - lat_min)/lat_step;

% generate surface velocity magnitude plot
% figure(1)
% transpose to match (long, lat, alt) coords
% vel_total_surf = vel_total(:,:,1)';
% % plot a colour map (vel_total(:, :, 1) is first layer)
% vel_map = pcolor(longitude,latitude,vel_total_surf);
% hold on
% coast_plot = plot(coastlon, coastlat, 'k');
% hold off
% vel_map.EdgeAlpha = 0;% remove the dark edges
% xlabel('Longitude (deg)');
% ylabel('Latitude (deg)');
% title('Horizontal Velocity Magnitude (m/s) at Surface over Data Region');
% colorbar;

% % horizontal wind vector field at surface
% u_surf = vel_u(:,:,1)';
% v_surf = vel_v(:,:,1)';
% figure(2);
% quiver(longitude,latitude,u_surf,v_surf)
% axis([long_min long_max lat_min, lat_max])
% hold on
% plot(coastlon, coastlat, 'k')
% hold off
% xlabel('Longitude (deg)');
% ylabel('Latitude (deg)');
% title('Surface layer velocity vectors')

% % surface temperature plot
% figure(3)
% surf_temp = surf_temp';
% temp_map = pcolor(longitude, latitude, surf_temp);
% hold on
% plot(coastlon, coastlat, 'k');
% hold off
% temp_map.EdgeAlpha = 0;
% xlabel('Longitude (deg)');
% ylabel('Latitude (deg)');
% title('Surface temperature (^{o}C)');
% colorbar;

% 'ridge plot' ??
% figure(4)
% ridge_map = pcolor(longitude, latitude, ridge');
% ridge_map.EdgeAlpha = 0;
% hold on
% plot(coastlon, coastlat, 'k');
% hold off
% xlabel('Longitude (deg)');
% ylabel('Latitude (deg)');
% title('Ridge');
% colorbar;

% cape plot
figure(5);
cape_map = pcolor(longitude, latitude, cape');
cape_map.EdgeAlpha = 0;
hold on
plot(coastlon, coastlat, 'k');
hold off
xlabel('Longitude (deg)');
ylabel('Latitude (deg)');
title('CAPE (J/kg)');
colorbar;
