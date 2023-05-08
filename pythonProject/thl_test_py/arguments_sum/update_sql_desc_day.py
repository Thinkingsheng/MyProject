# -*- coding:utf-8 -*-

day_update_1 = [
    {
        'delete_sql': """
DELETE FROM `dim_holiday_weather_day`;
        """,
        'append_table': 'dim_holiday_weather_day',
        'data_sql': """
SELECT
	`day`
	,`week_num`
	,`work_day`
	,`festival`
	,IF(`festival_or`='',null,festival_or) as `festival_or`
	,`festival_today`
	,`holiday_festival`
	,`weather`
	,city_epidemic_count
FROM
	dim_holiday_weather_day_1
        """
    },
    {
        'delete_sql': """
DELETE FROM `dm_consumer_flow_epidemic_day`;
    """,
        'append_table': 'dm_consumer_flow_epidemic_day',
        'data_sql': """
	SELECT
		t1.`day`,
		ROUND(t1.`number`/10000,2) as `consumer_number`,
		t2.city_epidemic_count
	FROM
		(
		SELECT
			`day`,
			`number`
		FROM
			dm_consumer_flow_arrive_day
		WHERE
			source = "all"
		)
		t1
		LEFT JOIN
		(
		SELECT
			`day`,
			city_epidemic_count
		FROM
			dim_holiday_weather_day_1
		)t2 ON t1.`day` = t2.`day`
	WHERE
		t1.`day` >= '2022-10-01'
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_consumer_flow_holiday_day`;
    """,
        'append_table': 'dm_consumer_flow_holiday_day',
        'data_sql': """
SELECT
	t1.`day`
	,t4.week_num
	,t4.holiday_explain
	,t1.`number` as consumer_number
	,ROUND((t1.`number` - t2.`number`)/t2.`number`,7) as ring_ratio
	,ROUND((t1.`number` - t3.`number`)/t3.`number`,7) as week_ratio
FROM
	(
	SELECT
		`day`
		,`number`
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	) t1
	INNER JOIN
	(
	SELECT
		`day`
		,`number`
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	)t2 ON t1.`day` = DATE_ADD(t2.`day`,INTERVAL 1 DAY)
	INNER JOIN
	(
	SELECT
		`day`
		,`number`
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	)t3 ON t1.`day` = DATE_ADD(t3.`day`,INTERVAL 7 DAY)
	INNER JOIN
	(
	SELECT
		`day`,
		week_num,
		(
		CASE
		WHEN festival <> "非节假日" and holiday_festival = 1 and festival_or <> "" THEN CONCAT(festival,"&",festival_or)
		WHEN festival <> "非节假日" and holiday_festival = 1 and festival_or = "" THEN festival
		WHEN week_num IN ("周六","周日") and work_day = 0 THEN "周末休息"
		ELSE "工作日"
		END
		)as holiday_explain
	FROM
		dim_holiday_weather_day_1
	)t4 ON t1.`day` = t4.`day`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_flow_weather_year_avg_day`;
    """,
        'append_table': 'dm_flow_weather_year_avg_day',
        'data_sql': """
	SELECT
		s1.sum_day as `day`,
		s2.weather,
		COUNT(weather) as weather_num,
		ROUND(SUM(s2.`number`)/COUNT(s2.weather)) as weather_avg_num
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					`day`
				FROM
					dm_consumer_flow_arrive_day
				WHERE
					source = "all"
				)r1 
				JOIN
				(
				SELECT
					`day`,
					DATE_SUB(`day`,interval 1 year) as day_before365
				FROM
					dm_consumer_flow_arrive_day
				WHERE
					source = "all"
				) r2 ON r1.`day` > r2.day_before365 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(`day`),interval 1 year) from dm_consumer_flow_arrive_day WHERE source = "all")
		) s1
		JOIN
		(
		SELECT
			z1.`day`,
			z1.`number`,
			z2.weather
		FROM
			(
			SELECT
				`day`,
				`number`
			FROM
				dm_consumer_flow_arrive_day
			WHERE
				source = "all"
			)z1
			INNER JOIN
			(
			SELECT
				`day`,
				weather
			FROM
				dim_holiday_weather_day_1
			)z2 ON z1.`day` = z2.`day`
		)s2 ON s1.range_day = s2.`day`
	GROUP BY
		s1.sum_day,
		s2.weather
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_source_percent_num_day`;
    """,
        'append_table': 'dm_source_percent_num_day',
        'data_sql': """
SELECT
	s1.`day`,
	s1.source,
	s1.`percent`,
	ROUND(s1.`percent` * s2.`number`) as `number`
FROM
	(
	SELECT
		t1.`day`,
		t1.source,
		TRUNCATE(t1.`count`/t2.`count`,18) as `percent`
	FROM
		(
		SELECT
			`day`,
			source,
			`number` as `count`
		FROM
			dm_consumer_flow_arrive_day
		WHERE
			source NOT IN ("","all","tourist")
		) t1
		INNER JOIN
		(
		SELECT
			`day`,
			sum(`number`) as `count`
		FROM
			dm_consumer_flow_arrive_day
		WHERE
			source NOT IN ("","all","tourist")
		GROUP BY
			`day`
		) t2 ON t1.`day` = t2.`day`
	UNION ALL
	SELECT
		`day`,
		"all" as source,
		TRUNCATE(1,18) as `percent`
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	GROUP BY
		`day`
	) s1
	INNER JOIN
	(
	SELECT
		`day`,
		`number`
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	GROUP BY
		`day`
	)s2 ON s1.`day` = s2.`day`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_origin_index_percent_day`;
    """,
        'append_table': 'dm_origin_index_percent_day',
        'data_sql': """
with t as (
SELECT
	date_format(t1.`date`,'%Y-%m') as `month`,
	t1.`date`,
	t1.source,
	t1.`type`,
	ROUND(t1.`percent`*t2.`number`,0) as `index`,
	TRUNCATE(t1.`percent`,18) as `percent`,
	t2.`number` as `day_number`
FROM
	(
	SELECT
		`day` as `date`,
		source,
		'guangzhou_inside' as `type`,
		`percent`
	FROM
		dm_district_image_geo_day
	WHERE
		`image` = "residentCity" and label = "residentCity" and `value` = '广州市'
		and
		source <> ""
	GROUP BY
		`date`,source
	
	UNION ALL
	
	-- 此处的广东省内，去除了广州
	SELECT
		s1.`day` as `date`,
		s1.source,
		'guangdong_inside' as `type`,
		(s1.`percent`-s2.`percent`) as `percent`
	FROM
		(
		SELECT
			`day`,
			source,
			SUM(`percent`) as `percent`
		FROM
			dm_district_image_geo_day
		WHERE
			`image` = "residentProvince" and label = "residentProvince" and `value` = '广东省'
			and
			source <> ""
		GROUP BY
			`day`,source
		) s1
		INNER JOIN
		(
		SELECT
			`day`,
			source,
			SUM(`percent`) as `percent`
		FROM
			dm_district_image_geo_day
		WHERE
			`image` = "residentCity" and label = "residentCity" and `value` = '广州市'
			and
			source <> ""
		GROUP BY
			`day`,source
		) s2 ON s1.`day` = s2.`day` and s1.source = s2.source
	
	UNION ALL

	-- 此处1-广东省作为省外
	SELECT
		`day` as `date`,
		source,
		'guangdong_outside' as `type`,
		1-SUM(`percent`) as `percent`
	FROM
		dm_district_image_geo_day
	WHERE
		`image` = "residentProvince" and label = "residentProvince" and `value` = '广东省'
		and
		source <> ""
	GROUP BY
		`date`,source
	) t1 INNER JOIN
	(
	SELECT
		`day`,
		source,
		`number`
	FROM
		dm_consumer_flow_arrive_day
	)t2 ON t1.`date` = t2.`day` and t1.source = t2.source
)
SELECT
	t1.`month`,
	t1.`date`,
	t1.source,
	t1.`type`,
	t1.`index`,
	t1.`percent`,
	t2.`index` as last_index,
	t2.`percent` as last_percent,
	t3.`index` as last_week_day_index,
	t3.`percent` as last_week_day_percent,
	t4.`index` as last_month_day_index,
	t4.`percent` as last_month_day_percent,
	t5.`index` as last_year_day_index,
	t5.`percent` as last_year_day_percent,
	truncate((t1.`index`-t2.`index`)/t2.`index`,18) as index_ring_ratio,
	truncate((t1.`index`-t3.`index`)/t3.`index`,18) as index_week_ratio,
	truncate((t1.`index`-t4.`index`)/t4.`index`,18) as index_month_ratio,
	truncate((t1.`index`-t5.`index`)/t5.`index`,18) as index_year_ratio,
	t1.`day_number`
FROM
	t t1 
	LEFT JOIN 
	t t2 ON t1.`date` = t2.`date` + INTERVAL 1 DAY and t1.source = t2.source and t1.`type` = t2.`type`
	LEFT JOIN 
	t t3 ON t1.`date` = t3.`date` + INTERVAL 7 DAY and t1.source = t3.source and t1.`type` = t3.`type`
	LEFT JOIN 
	t t4 ON t1.`date` = t4.`date` + INTERVAL 30 DAY and t1.source = t4.source and t1.`type` = t4.`type`
	LEFT JOIN 
	t t5 ON t1.`date` = str_to_date(CONCAT(date_format(t5.`date`,"%Y")+1,"-",date_format(t5.`date`,"%m-%d")),"%Y-%m-%d") and t1.source = t5.source and t1.`type` = t5.`type`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_consumer_flow_arrive_month`;
    """,
        'append_table': 'dm_consumer_flow_arrive_month',
        'data_sql': """
with t as (
SELECT
	cast(date_format(`day`,'%Y%m')as unsigned) as `month`,
	sum(`number`) as `number`,
	sum(mentimes) as mentimes,
	sum(IFNULL(number_population,0)) as number_population,
	sum(IFNULL(mentimes_population,0)) as mentimes_population,
	source
FROM
	dm_consumer_flow_arrive_day
GROUP BY
	`month`,source
)

SELECT
	t1.`month`,
	t1.`number`,
	t2.`number` as last_month_number,
	t3.`number` as last_year_month_number,
	truncate((t1.`number`-t2.`number`)/t2.`number`,18) as number_ring_ratio,
	truncate((t1.`number`-t3.`number`)/t3.`number`,18) as number_year_ratio,
	t1.mentimes,
	t1.number_population,
	t1.mentimes_population,
	t1.source
FROM
	t t1
	LEFT JOIN
	t t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.source = t2.source
	LEFT JOIN 
	t t3 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t3.`month`,'01'),'%Y%m%d'),INTERVAL 1 YEAR) AND t1.source = t3.source
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_origin_index_city_day`;
    """,
        'append_table': 'dm_origin_index_city_day',
        'data_sql': """
SELECT
	s1.`day` as `date`,
	s1.source,
	(CASE
	WHEN s3.city_name IS NOT NULL THEN "省内"
	WHEN s3.city_name IS NULL THEN "省外"
	END) as city_type,
	s1.city,
	ROUND(s2.`number`*s1.`percent`,0) as `city_number`,
	truncate(s1.`percent`,18) as `city_percent`,
	s2.`number` as `day_number`
FROM
	(
	SELECT
		`day`,
		`source`,
		`value` as city,
		`percent`
	FROM
		dm_district_image_geo_day
	WHERE
		`image` = "residentCity" and label = "residentCity"
		and 
		`value` <> ""
	) s1
	INNER JOIN
	(
	SELECT
		`day`,
		source,
		`number`
	FROM
		dm_consumer_flow_arrive_day
	)s2 ON s1.`day` = s2.`day` and s1.`source` = s2.`source`
	LEFT JOIN 
	dim_guangdong_city_name s3 on s1.city = s3.city_name 
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_source_percent_num_month`;
    """,
        'append_table': 'dm_source_percent_num_month',
        'data_sql': """
	SELECT
		s1.`month`,
		REPLACE(s1.`month`,"-","") as month_2,
		s1.source,
		s1.`percent`,
		ROUND(s1.`percent` * s2.`number`) as `number`
	FROM
		(
		SELECT
			t1.`month`,
			t1.source,
			TRUNCATE(t1.`count`/t2.`count`,18) as `percent`
		FROM
			(
			SELECT
				date_format(`day`,"%Y-%m") as `month`,
				source,
				sum(`number`) as `count`
			FROM
				dm_consumer_flow_arrive_day
			WHERE
				source NOT IN ("","all","tourist")
			GROUP BY
				`month`,
				source
			) t1
			INNER JOIN
			(
			SELECT
				date_format(`day`,"%Y-%m") as `month`,
				sum(`number`) as `count`
			FROM
				dm_consumer_flow_arrive_day
			WHERE
				source NOT IN ("","all","tourist")
			GROUP BY
				`month`
			) t2 ON t1.`month` = t2.`month`
		UNION ALL
		SELECT
			date_format(str_to_date(CONCAT(cast(`month` as char),'01'),'%Y%m%d'),'%Y-%m') as `month`,
			"all" as source,
			TRUNCATE(1,18) as `percent`
		FROM
			dm_consumer_flow_arrive_month
		WHERE
			source = "all"
		GROUP BY
			date_format(str_to_date(CONCAT(cast(`month` as char),'01'),'%Y%m%d'),'%Y-%m')
		)s1
		INNER JOIN
		(
		SELECT
			`month`,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		WHERE
			source = "all"
		) s2 ON REPLACE(s1.`month`,"-","") = CAST(s2.`month` AS char)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_source_stay_duration_day`;
    """,
        'append_table': 'dm_source_stay_duration_day',
        'data_sql': """
SELECT
	t1.`day`,
	'all' as source,
	t1.duration,
	TRUNCATE(sum(t1.`percent`*t2.`percent`),18) as `percent`
FROM
	dm_stay_duration_day t1
	INNER JOIN
	dm_source_percent_num_month t2 ON (date_format(t1.`day`,"%Y-%m") = t2.`month` and CONVERT(t1.source USING UTF8) = t2.source)
GROUP BY
	t1.`day`,
	t1.duration
UNION ALL
SELECT
	`day`,
	source,
	duration,
	`percent`
FROM
	dm_stay_duration_day
WHERE
	source <> ""
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_consumer_flow_year_avg_week`;
    """,
        'append_table': 'dm_consumer_flow_year_avg_week',
        'data_sql': """
	SELECT
		s1.sum_day as `day`,
		s2.week_str,
		s2.week_num,
		ROUND(SUM(s2.`number`)/COUNT(week_num)) as week_avg_num
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			-- 一个sum_day对应过去365个range_day
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					`day`
				FROM
					dm_consumer_flow_arrive_day
				WHERE
					source = "all"
				)r1 
				JOIN
				(
				SELECT
					`day`,
					DATE_SUB(`day`,interval 1 year) as day_before365
				FROM
					dm_consumer_flow_arrive_day
				WHERE
					source = "all"
				) r2 ON r1.`day` > r2.day_before365 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(`day`),interval 1 year) from dm_consumer_flow_arrive_day WHERE source = "all")
		) s1
		JOIN
		(
		SELECT
			`day`,
			(CASE 
			WHEN dayofweek(`day`) = 2 THEN "周一"
			WHEN dayofweek(`day`) = 3 THEN "周二"
			WHEN dayofweek(`day`) = 4 THEN "周三"
			WHEN dayofweek(`day`) = 5 THEN "周四"
			WHEN dayofweek(`day`) = 6 THEN "周五"
			WHEN dayofweek(`day`) = 7 THEN "周六"
			WHEN dayofweek(`day`) = 1 THEN "周日"
			END) as week_str,
			weekday(`day`) as week_num,
			`number`
		FROM
			dm_consumer_flow_arrive_day
		WHERE
			source = "all"
		)s2 ON s1.range_day = s2.`day`
	GROUP BY
		s1.sum_day,
		s2.week_str,
		s2.week_num
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_zhengjia_flow_factor_day`;
        """,
        'append_table': 'dm_zhengjia_flow_factor_day',
        'data_sql': """
SELECT
	t2.`day`,
	t1.`number` as zj_number,
	TRUNCATE(t1.`number`/(t2.`number` - IFNULL(t2.number_population,0)),15) as zj_factor
FROM
	(
	SELECT
		*
	FROM
		dm_yingyun_zhengjia_flow_arrive_day
	) t1
	INNER JOIN
	(
	SELECT
		*
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	) t2 ON str_to_date(t1.`day`,'%Y%m%d') = t2.`day`
        """
    },
    {
        'delete_sql': """
DELETE FROM `dm_zhengjia_flow_factor_week`;
    """,
        'append_table': 'dm_zhengjia_flow_factor_week',
        'data_sql': """
SELECT
	t1.week_num,
	t1.week_start_date,
	t1.zj_number,
	TRUNCATE(t1.zj_number/t2.ta_number,15) as zj_factor
FROM
	(
	SELECT
		date_format(str_to_date(`day`,'%Y%m%d'),'%v') as week_num,
		date(subdate(str_to_date(`day`,'%Y%m%d'), (date_format(str_to_date(`day`,'%Y%m%d'),'%w')+6)%7)) as week_start_date,
		sum(`number`) as zj_number
	FROM
		dm_yingyun_zhengjia_flow_arrive_day
	GROUP BY
		week_num,week_start_date
	) t1
	INNER JOIN
	(
	SELECT
		date_format(`day`,'%v') as week_num,
		date(subdate(`day`, (date_format(`day`,'%w')+6)%7)) as week_start_date,
		sum((`number` - IFNULL(number_population,0))) as ta_number
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	GROUP BY
		week_num,week_start_date
	) t2 ON t1.week_num = t2.week_num and t1.week_start_date = t2.week_start_date
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_order_target_day`;
    """,
        'append_table': 'dm_order_target_day',
        'data_sql': """
SELECT
	t1.`day`,
	t2.order_count,
	-- 固定比例1人下1.3单
	ROUND(t2.order_count/1.3) as order_user_count,
	t2.gmv,
	ROUND(t2.gmv/t2.order_count,2) as cus_unit_price,
	TRUNCATE(t2.order_count/t1.original_number,15) as bag_carry_rate
FROM
	(
	SELECT
		`day`,
		-- 加人口后的值减去人口数，变回原数值
		`number` - IFNULL(number_population,0) as original_number
	FROM
		dm_consumer_flow_arrive_day
	WHERE
		source = "all"
	)t1
	INNER JOIN
	(
	SELECT
		date(`create_at`) as `day`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`
	)t2 ON t1.`day` = t2.`day`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_order_target_amount_range`;
    """,
        'append_table': 'dm_order_target_amount_range',
        'data_sql': """
SELECT
	t1.`day`,
	t1.amount_range,
	t1.order_count,
	t1.order_user_count,
	t1.order_count_percent,
	t2.order_count_30day,
	t2.order_user_count_30day,
	t2.order_count_30day_percent

FROM
	(
	-- 订单数、订单人数、笔数占比
	SELECT
		s1.`day`,
		s1.amount_range,
		s1.order_count,
		s1.order_user_count,
		TRUNCATE(s1.order_count/s2.order_count,19) as order_count_percent
	FROM
		(
		SELECT
			date(`create_at`) as `day`,
			(CASE
			WHEN amount > 0 and amount <= 200 THEN "0-200元"
			WHEN amount > 200 and amount <= 500 THEN "200-500元"
			WHEN amount > 500 and amount <= 1000 THEN "500-1000元"
			WHEN amount > 1000 and amount <= 2000 THEN "1000-2000元"
			WHEN amount > 2000 and amount <= 4000 THEN "2000-4000元"
			WHEN amount > 4000 and amount <= 10000 THEN "4000-10000元"
			ELSE "10000元以上"
			END) as amount_range,
			count(order_num) as order_count,
			count(order_num) as order_user_count
		FROM
			zhengjia_sale_data
		WHERE
			pay_status = "交易成功"
		GROUP BY
			`day`,amount_range
		) s1
		LEFT JOIN
		(
		SELECT
			date(`create_at`) as `day`,
			count(order_num) as order_count
		FROM
			zhengjia_sale_data
		WHERE
			pay_status = "交易成功"
		GROUP BY
			`day`
		) s2 ON s1.`day` = s2.`day`
	) t1	
	LEFT JOIN
	(
	-- 30天平均订单数、30日平均订单人数
	SELECT
		s1.sum_day as `day`,
		s2.amount_range,
		ROUND(avg(s2.order_count),0) as order_count_30day,
		ROUND(avg(s2.order_user_count),0) as order_user_count_30day,
		-- 30日平均笔数占比 = 30天内区间总笔数/30天内总笔数
		TRUNCATE(sum(s2.order_count)/sum(s3.order_count),19) as order_count_30day_percent
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					date(`create_at`) as `day`
				FROM
					zhengjia_sale_data
				WHERE
					pay_status = "交易成功"
				GROUP BY
					`day`
				)r1 
				JOIN
				(
				SELECT
					date(`create_at`) as `day`,
					DATE_SUB(date(`create_at`),interval 30 day) as day_before30
				FROM
					zhengjia_sale_data
				WHERE
					pay_status = "交易成功"
				GROUP BY
					`day`
				) r2 ON r1.`day` > r2.day_before30 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(date(`create_at`)),interval 30 day) from zhengjia_sale_data)
		)s1 
		JOIN
		(
		SELECT
			date(`create_at`) as `day`,
			(CASE
			WHEN amount > 0 and amount <= 200 THEN "0-200元"
			WHEN amount > 200 and amount <= 500 THEN "200-500元"
			WHEN amount > 500 and amount <= 1000 THEN "500-1000元"
			WHEN amount > 1000 and amount <= 2000 THEN "1000-2000元"
			WHEN amount > 2000 and amount <= 4000 THEN "2000-4000元"
			WHEN amount > 4000 and amount <= 10000 THEN "4000-10000元"
			ELSE "10000元以上"
			END) as amount_range,
			count(order_num) as order_count,
			count(order_num) as order_user_count
		FROM
			zhengjia_sale_data
		WHERE
			pay_status = "交易成功"
		GROUP BY
			`day`,amount_range
		) s2 ON s1.range_day = s2.`day`
		JOIN
		(
		SELECT
			date(`create_at`) as `day`,
			count(order_num) as order_count
		FROM
			zhengjia_sale_data
		WHERE
			pay_status = "交易成功"
		GROUP BY
			`day`
		) s3 ON s1.range_day = s3.`day`
	GROUP BY
		s1.sum_day,s2.amount_range
	) t2 ON (t1.`day` = t2.`day` and t1.amount_range = t2.amount_range)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_order_gmv_year_avg_week`;
    """,
        'append_table': 'dm_order_gmv_year_avg_week',
        'data_sql': """
	SELECT
		s1.sum_day as `day`,
		s2.week_str,
		s2.week_num,
		ROUND(SUM(s2.`gmv`)/COUNT(s2.week_num),2) as week_avg_num
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			-- 一个sum_day对应过去365个range_day
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					`day`
				FROM
					dm_ta_order_target_day
				)r1 
				JOIN
				(
				SELECT
					`day`,
					DATE_SUB(`day`,interval 1 year) as day_before365
				FROM
					dm_ta_order_target_day
				) r2 ON r1.`day` > r2.day_before365 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(`day`),interval 1 year) from dm_ta_order_target_day)
		) s1
		JOIN
		(
		SELECT
			`day`,
			(CASE 
			WHEN dayofweek(`day`) = 2 THEN "周一"
			WHEN dayofweek(`day`) = 3 THEN "周二"
			WHEN dayofweek(`day`) = 4 THEN "周三"
			WHEN dayofweek(`day`) = 5 THEN "周四"
			WHEN dayofweek(`day`) = 6 THEN "周五"
			WHEN dayofweek(`day`) = 7 THEN "周六"
			WHEN dayofweek(`day`) = 1 THEN "周日"
			END) as week_str,
			weekday(`day`) as week_num,
			`gmv`
		FROM
			dm_ta_order_target_day
		)s2 ON s1.range_day = s2.`day`
	GROUP BY
		s1.sum_day,
		s2.week_str,
		s2.week_num
    """
    },
    {
        'delete_sql': """
DELETE FROM `ods_unionpay_order_target_month`;
    """,
        'append_table': 'ods_unionpay_order_target_month',
        'data_sql': """
SELECT
	substr(cast(t1.`day` as char),1,6) as `month`,
	SUM(t1.gmv) as gmv,
	SUM(t1.order_count) as order_count,
	SUM(t1.order_user_count) as order_user_count
FROM
	ods_unionpay_order_target_day t1
GROUP BY
	`month`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_unionpay_order_target_hour_range`;
    """,
        'append_table': 'dm_unionpay_order_target_hour_range',
        'data_sql': """
with t as (
SELECT
	str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`,
	ROUND(zero_six_order_count_percent * order_count) as zero_six_order_count,
	ROUND(six_twelve_order_count_percent * order_count) as six_twelve_order_count,
	ROUND(twelve_eighteen_order_count_percent * order_count) as twelve_eighteen_order_count,
	ROUND(eighteen_twentyfour_order_count_percent * order_count) as eighteen_twentyfour_order_count,
	ROUND(zero_six_gmv_percent * gmv,2) as zero_six_gmv,
	ROUND(six_twelve_gmv_percent * gmv,2) as six_twelve_gmv,
	ROUND(twelve_eighteen_gmv_percent * gmv,2) as twelve_eighteen_gmv,
	ROUND(eighteen_twentyfour_gmv_percent * gmv,2) as eighteen_twentyfour_gmv,
	ROUND(zero_six_order_user_count_percent * order_user_count) as zero_six_order_user_count,
	ROUND(six_twelve_order_user_count_percent * order_user_count) as six_twelve_order_user_count,
	ROUND(twelve_eighteen_order_user_count_percent * order_user_count) as twelve_eighteen_order_user_count,
	ROUND(eighteen_twentyfour_order_user_count_percent * order_user_count) as eighteen_twentyfour_order_user_count
FROM
	ods_unionpay_order_target_day t1
	INNER JOIN 
	ods_unionpay_order_percent_hour_range t2 ON t1.`day` = t2.`day`
)

SELECT
	t1.`day`,
	'0-6点' as `hour_range`,
	t1.zero_six_order_count as order_count,
	t2.zero_six_order_count as yes_order_count,
	t1.zero_six_gmv as gmv,
	t2.zero_six_gmv as yes_gmv,
	t1.zero_six_order_user_count as order_user_count,
	t2.zero_six_order_user_count as yes_order_user_count
FROM
	t t1
	INNER JOIN
	t t2 ON t1.`day` = DATE_ADD(t2.`day`,interval 1 day)
UNION ALL
SELECT
	t1.`day`,
	'6-12点' as `hour_range`,
	t1.six_twelve_order_count as order_count,
	t2.six_twelve_order_count as yes_order_count,
	t1.six_twelve_gmv as gmv,
	t2.six_twelve_gmv as yes_gmv,
	t1.six_twelve_order_user_count as order_user_count,
	t2.six_twelve_order_user_count as yes_order_user_count
FROM
	t t1
	INNER JOIN
	t t2 ON t1.`day` = DATE_ADD(t2.`day`,interval 1 day)
UNION ALL
SELECT
	t1.`day`,
	'12-18点' as `hour_range`,
	t1.twelve_eighteen_order_count as order_count,
	t2.twelve_eighteen_order_count as yes_order_count,
	t1.twelve_eighteen_gmv as gmv,
	t2.twelve_eighteen_gmv as yes_gmv,
	t1.twelve_eighteen_order_user_count as order_user_count,
	t2.twelve_eighteen_order_user_count as yes_order_user_count
FROM
	t t1
	INNER JOIN
	t t2 ON t1.`day` = DATE_ADD(t2.`day`,interval 1 day)
UNION ALL
SELECT
	t1.`day`,
	'18-24点' as `hour_range`,
	t1.eighteen_twentyfour_order_count as order_count,
	t2.eighteen_twentyfour_order_count as yes_order_count,
	t1.eighteen_twentyfour_gmv as gmv,
	t2.eighteen_twentyfour_gmv as yes_gmv,
	t1.eighteen_twentyfour_order_user_count as order_user_count,
	t2.eighteen_twentyfour_order_user_count as yes_order_user_count
FROM
	t t1
	INNER JOIN
	t t2 ON t1.`day` = DATE_ADD(t2.`day`,interval 1 day)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_unionpay_order_target_amount_range`;
    """,
        'append_table': 'dm_unionpay_order_target_amount_range',
        'data_sql': """
with t as (
SELECT
	t1.`day`,
	t1.cus_unit_price_range,
	t1.gmv_percent*t2.gmv as gmv,
	t1.order_count_percent*t2.order_count as order_count,
	t1.order_user_count_percent*t2.order_user_count as order_user_count
FROM
	ods_unionpay_cus_unit_percent_day t1
	INNER JOIN
	ods_unionpay_order_target_day t2 ON t1.`day` = t2.`day`
)

SELECT
	x1.`day`,
	x1.cus_unit_price_range,
	x1.order_count,
	x1.order_user_count,
	x1.order_count_percent,
	x2.order_count_30day,
	x2.order_user_count_30day,
	x2.order_count_30day_percent
FROM
	(
	-- 订单数、订单人数、笔数占比
	SELECT
		str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`,
		t1.cus_unit_price_range,
		ROUND(t1.order_count) as order_count,
		ROUND(t1.order_user_count) as order_user_count,
		t1.order_count/t2.order_count as order_count_percent
	FROM
		t t1
		INNER JOIN
		ods_unionpay_order_target_day t2 ON t1.`day` = t2.`day`
	) x1
	LEFT JOIN
	(
	-- 30天平均订单数、30日平均订单人数、30日平均笔数占比
	SELECT
		s1.sum_day as `day`,
		s2.cus_unit_price_range,
		ROUND(avg(s2.order_count),0) as order_count_30day,
		ROUND(avg(s2.order_user_count),0) as order_user_count_30day,
		-- 30日平均笔数占比 = 30天内区间总笔数/30天内总笔数
		TRUNCATE(sum(s2.order_count)/sum(s3.order_count),19) as order_count_30day_percent
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`
				FROM
					ods_unionpay_order_target_day t1
				GROUP BY
					t1.`day`
				)r1 
				JOIN
				(
				SELECT
					str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`,
					DATE_SUB(str_to_date(cast(t1.`day` as char),'%Y%m%d'),interval 30 day) as day_before30
				FROM
					ods_unionpay_order_target_day t1
				GROUP BY
					t1.`day`
				) r2 ON r1.`day` > r2.day_before30 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(str_to_date(cast(`day` as char),'%Y%m%d')),interval 30 day) from ods_unionpay_order_target_day)
		)s1 
		JOIN
		t s2 ON s1.range_day = str_to_date(cast(s2.`day` as char),'%Y%m%d')
		JOIN
		ods_unionpay_order_target_day s3 ON s1.range_day = str_to_date(cast(s3.`day` as char),'%Y%m%d')
	GROUP BY
		s1.sum_day,s2.cus_unit_price_range
	) x2 ON (x1.`day` = x2.`day` and x1.cus_unit_price_range = x2.cus_unit_price_range)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_unionpay_order_gmv_year_avg_week`;
    """,
        'append_table': 'dm_unionpay_order_gmv_year_avg_week',
        'data_sql': """
	SELECT
		s1.sum_day as `day`,
		s2.week_str,
		s2.week_num,
		ROUND(SUM(s2.`gmv`)/COUNT(s2.week_num),2) as week_avg_num
	FROM
		(
		-- 日期维表
		SELECT
			z1.sum_day,
			z1.range_day
		FROM
			(
			-- 一个sum_day对应过去365个range_day
			SELECT
				r2.`day` as sum_day,
				r1.`day` as range_day
			FROM
				(
				SELECT
					str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`
				FROM
					ods_unionpay_order_target_day t1
				GROUP BY
					t1.`day`
				)r1 
				JOIN
				(
				SELECT
					str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`,
					DATE_SUB(str_to_date(cast(t1.`day` as char),'%Y%m%d'),interval 1 year) as day_before365
				FROM
					ods_unionpay_order_target_day t1
				GROUP BY
					t1.`day`
				) r2 ON r1.`day` > r2.day_before365 and r1.`day` <= r2.`day`
			) z1
		WHERE
			z1.sum_day >= (select DATE_ADD(min(str_to_date(cast(`day` as char),'%Y%m%d')),interval 1 year) from ods_unionpay_order_target_day)
		) s1
		JOIN
		(
		SELECT
			str_to_date(cast(t1.`day` as char),'%Y%m%d') as `day`,
			(CASE 
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 2 THEN "周一"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 3 THEN "周二"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 4 THEN "周三"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 5 THEN "周四"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 6 THEN "周五"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 7 THEN "周六"
			WHEN dayofweek(str_to_date(cast(t1.`day` as char),'%Y%m%d')) = 1 THEN "周日"
			END) as week_str,
			weekday(str_to_date(cast(t1.`day` as char),'%Y%m%d')) as week_num,
			t1.`gmv`
		FROM
			ods_unionpay_order_target_day t1
		)s2 ON s1.range_day = s2.`day`
	GROUP BY
		s1.sum_day,
		s2.week_str,
		s2.week_num
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_unionpay_sex_user_percent_month`;
    """,
        'append_table': 'dm_unionpay_sex_user_percent_month',
        'data_sql': """
with t as (
SELECT
	s1.`month`,
	s1.sex,
	ROUND(s1.user_count) as user_count,
	s1.user_count/s2.order_user_count as `percent`,
	ROUND(s1.order_count) as order_count,
	s1.order_count/s2.order_count as order_count_percent,
	ROUND(s1.gmv,2) as gmv,
	s1.gmv/s2.gmv as gmv_percent
FROM
	(
	-- 计算出日的消费用户性别分布，再转为月，与月的总消费用户连表
	SELECT
		substr(cast(t1.`day` as char),1,6) as `month`,
		t1.sex,
		sum(t1.order_user_count_percent*t2.order_user_count) as user_count,
		sum(t3.order_count) as order_count,
		sum(t3.gmv) as gmv
	FROM
		ods_unionpay_sex_user_percent_day t1
		INNER JOIN
		ods_unionpay_order_target_day t2 ON t1.`day` = t2.`day`
		INNER JOIN 
		ods_unionpay_sex_order_percent_day t3 ON t1.`day` = t3.`day` and t1.`sex` = t3.`sex`
	GROUP BY
		`month`,
		t1.sex
	) s1
	INNER JOIN
	(
	SELECT
		`month`,
		order_user_count,
		order_count,
		gmv
	FROM
		ods_unionpay_order_target_month_v
	) s2 ON s1.`month` = s2.`month`
)

SELECT
	t1.`month`,
	t1.`sex`,
	t1.user_count,
	truncate((t1.user_count-t2.user_count)/t2.user_count,18) as user_count_ring_ratio,
	truncate((t1.user_count-t3.user_count)/t3.user_count,18) as user_count_year_ratio,
	truncate(t1.`percent`,18) as `percent`,
	t1.order_count,
	truncate((t1.order_count-t2.order_count)/t2.order_count,18) as order_count_ring_ratio,
	truncate((t1.order_count-t3.order_count)/t3.order_count,18) as order_count_year_ratio,
	truncate(t1.`order_count_percent`,18) as `order_count_percent`,
	t1.gmv,
	truncate((t1.gmv-t2.gmv)/t2.gmv,18) as gmv_ring_ratio,
	truncate((t1.gmv-t3.gmv)/t3.gmv,18) as gmv_year_ratio,
	truncate(t1.`gmv_percent`,18) as `gmv_percent`
FROM
	t t1
	LEFT JOIN
	t t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.sex = t2.sex
	LEFT JOIN 
	t t3 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t3.`month`,'01'),'%Y%m%d'),INTERVAL 1 YEAR) AND t1.sex = t3.sex
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_unionpay_origin_order_percent_month`;
    """,
        'append_table': 'dm_unionpay_origin_order_percent_month',
        'data_sql': """
with t as (
SELECT
	s1.`month`,
	s1.origin_label,
	ROUND(s1.user_count) as user_count,
	s1.user_count/s2.order_user_count as `percent`,
	ROUND(s1.order_count) as order_count,
	s1.order_count/s2.order_count as `order_count_percent`,
	ROUND(s1.gmv,2) as gmv,
	s1.gmv/s2.gmv as `gmv_percent`
FROM
	(
	SELECT
		substr(cast(t1.`day` as char),1,6) as `month`,
		t1.origin_label,
		sum(t1.order_user_count_percent*t2.order_user_count) as user_count,
		sum(t1.order_count_percent*t2.order_count) as order_count,
		sum(t1.gmv_percent*t2.gmv) as gmv
	FROM
		ods_unionpay_origin_order_percent_day t1
		INNER JOIN
		ods_unionpay_order_target_day t2 ON t1.`day` = t2.`day`
	GROUP BY
		`month`,
		t1.origin_label
	) s1
	INNER JOIN
	(
	SELECT
		`month`,
		order_user_count,
		order_count,
		gmv
	FROM
		ods_unionpay_order_target_month_v
	) s2 ON s1.`month` = s2.`month`
)

SELECT
	t1.`month`,
	t1.`origin_label`,
	t1.user_count,
	truncate((t1.user_count-t2.user_count)/t2.user_count,18) as user_count_ring_ratio,
	truncate((t1.user_count-t3.user_count)/t3.user_count,18) as user_count_year_ratio,
	truncate(t1.`percent`,18) as `percent`,
	t1.order_count,
	truncate((t1.order_count-t2.order_count)/t2.order_count,18) as order_count_ring_ratio,
	truncate((t1.order_count-t3.order_count)/t3.order_count,18) as order_count_year_ratio,
	truncate(t1.`order_count_percent`,18) as `order_count_percent`,
	t1.gmv,
	truncate((t1.gmv-t2.gmv)/t2.gmv,18) as gmv_ring_ratio,
	truncate((t1.gmv-t3.gmv)/t3.gmv,18) as gmv_year_ratio,
	truncate(t1.`gmv_percent`,18) as `gmv_percent`
FROM
	t t1
	LEFT JOIN
	t t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.origin_label = t2.origin_label
	LEFT JOIN 
	t t3 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t3.`month`,'01'),'%Y%m%d'),INTERVAL 1 YEAR) AND t1.origin_label = t3.origin_label
    """
    }
]


day_update_2 = [
    {
        'delete_sql': """
DELETE FROM `dm_order_target_month`;
    """,
        'append_table': 'dm_order_target_month',
        'data_sql': """
SELECT
	t1.`month`,
	t2.order_count,
	t2.order_count as order_user_count,
	t2.gmv,
	ROUND(t2.gmv/t2.order_count,2) as cus_unit_price,
	TRUNCATE(t2.order_count/t1.original_number,15) as bag_carry_rate
FROM
	(
	SELECT
		`month`,
		-- 加人口后的值减去人口数，变回原数值
		`number` - IFNULL(number_population,0) as original_number
	FROM
		dm_consumer_flow_arrive_month
	WHERE
		source = "all"
	)t1
	INNER JOIN
	(
	select
		date_format(`create_at`,'%Y%m') as `month`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`month`
	)t2 ON CAST(t1.`month` AS CHAR) = t2.`month`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_zhengjia_flow_factor_month`;
    """,
        'append_table': 'dm_zhengjia_flow_factor_month',
        'data_sql': """
SELECT
	t1.`month`,
	t1.zj_number,
	TRUNCATE(t1.zj_number/t2.ta_number,15) as zj_factor
FROM
	(
	SELECT
		date_format(str_to_date(`day`,'%Y%m%d'),'%Y-%m') as `month`,
		sum(`number`) as zj_number
	FROM
		dm_yingyun_zhengjia_flow_arrive_day
	GROUP BY
		`month`
	) t1
	INNER JOIN
	(
	SELECT
		date_format(str_to_date(cast(`month` as char),'%Y%m%d'),'%Y-%m') as `month`,
		`number` - IFNULL(number_population,0) as ta_number
	FROM
		dm_consumer_flow_arrive_month
	WHERE
		source = "all"
	) t2 ON t1.`month` = t2.`month`
    """
    }
]
