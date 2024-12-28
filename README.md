# iotshop-backend
 圖片看[這裡](https://github.com/YuTengHuang/iot_vue)
 
 ## 關於nginx

在安裝好nginx後 `/etc/nginx/nginx.conf`的http裡要新增 `include /etc/nginx/sites-enabled/*;` \
並註解或移除 `include /etc/nginx/conf.d/*.conf;`
\
\
\
1.**目錄結構** \
`/etc/nginx/sites-available` 用來存放每個服務的設定檔

`/etc/nginx/sites-enabled`  用來放要啟用的服務的設定檔，在此資料夾底下建立 symbolic link 連結到 `/etc/nginx/sites-available` 底下的設定檔。
\
\
\
2. **連接文件** \
`/sites-available/example.conf` 建置好後 打指令
	
	sudo ln -s /etc/nginx/sites-available/example.conf /etc/nginx/sites-enabled/
	
就會連接檔案至`/sites-enabled/`底下。
\
\
\
3.**更新配置** \
若要替換conf則在`/sites-enabled/`底下刪除要替換的conf
並且在`/sites-available/`新增另一個新的conf然後打指令
	
	sudo ln -s /etc/nginx/sites-available/{替換的}.conf /etc/nginx/sites-enabled/
\
圖例:

	sites-available
		|
		|__ default
		|
		|__ example.conf
		|
		|__ new_example.conf <<<< sudo ln -s /etc/nginx/sites-available/new_example.conf /etc/nginx/sites-enabled/ 

            //連結新的conf至sites-enabled
	
	sites-enabled
		|
		|__ default
		|
		|__ example.conf   <<<< sudo rm /etc/nginx/sites-enabled/example.conf 移除不要啟用的conf
		|
		|__ new_example.conf 
