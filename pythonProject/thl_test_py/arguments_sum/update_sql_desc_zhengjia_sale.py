# -*- coding:utf-8 -*-

# 正佳的销售数据更新
zhengjia_sale_update = [
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
DELETE FROM `dm_b_type_order_target_day`;
        """,
        'append_table': 'dm_b_type_order_target_day',
        'data_sql': """
SELECT
	t1.`day`,
	t2.b_type,
	SUM(t1.order_count) as order_count,
	SUM(t1.order_count) as order_user_count,
	SUM(t1.gmv) as gmv
FROM
	(
	select
		date_format(`create_at`,'%Y%m%d') as `day`,
		store_num,
		store_name,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,store_num,store_name
	)t1
	INNER JOIN dm_store_b_type_info t2 
	ON t1.store_num = t2.store_num and t1.store_name = t2.store_name
GROUP BY
	t1.`day`,t2.b_type
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_b_type_order_target_week`;
        """,
        'append_table': 'dm_b_type_order_target_week',
        'data_sql': """
SELECT
	t1.week_num,
	t1.week_start_date,
	t1.week_section,
	t2.b_type,
	SUM(t1.order_count) as order_count,
	SUM(t1.order_count) as order_user_count,
	SUM(t1.gmv) as gmv
FROM
	(
	select
		date_format(`create_at`,'%v') as `week_num`,
		date(subdate(`create_at`, (date_format(`create_at`,'%w')+6)%7)) as week_start_date,
		CONCAT(date(subdate(`create_at`, (date_format(`create_at`,'%w')+6)%7)),"~",date(subdate(`create_at`, (date_format(`create_at`,'%w')-7)%7))) as week_section,
		store_num,
		store_name,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`week_num`,week_start_date,store_num,store_name
	)t1
	INNER JOIN dm_store_b_type_info t2 
	ON t1.store_num = t2.store_num and t1.store_name = t2.store_name
GROUP BY
	t1.`week_num`,t1.week_start_date,t1.week_section,t2.b_type
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_b_type_order_target_month`;
        """,
        'append_table': 'dm_b_type_order_target_month',
        'data_sql': """
SELECT
	t1.`month`,
	t2.b_type,
	SUM(t1.order_count) as order_count,
	SUM(t1.order_count) as order_user_count,
	SUM(t1.gmv) as gmv
FROM
	(
	select
		date_format(`create_at`,'%Y%m') as `month`,
		store_num,
		store_name,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`month`,store_num,store_name
	)t1
	INNER JOIN dm_store_b_type_info t2 
	ON t1.store_num = t2.store_num and t1.store_name = t2.store_name
GROUP BY
	t1.`month`,t2.b_type
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_order_target_hour`;
        """,
        'append_table': 'dm_order_target_hour',
        'data_sql': """
SELECT
	t1.`day`,
	t1.`hour`,
	t1.order_count,
	TRUNCATE((t1.order_count - t2.order_count)/t2.order_count,15) as order_count_chain_ratio,
	t1.gmv,
	TRUNCATE((t1.gmv - t2.gmv)/t2.gmv,15) as gmv_chain_ratio
	
FROM
	(
	SELECT
		date(`create_at`) as `day`,
		hour(`create_at`) as `hour`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,`hour`
	)t1 
	LEFT JOIN
	(
	SELECT
		date(`create_at`) as `day`,
		hour(`create_at`) as `hour`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,`hour`
	) t2
	ON (t1.`day` = DATE_ADD(t2.`day`,interval 1 day)) and (t1.`hour` = t2.`hour`)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_order_target_hour_range`;
        """,
        'append_table': 'dm_order_target_hour_range',
        'data_sql': """
SELECT
	t1.`day`,
	(CASE 
	WHEN t1.`hour` >= 1 and t1.`hour` <= 4 THEN "1-4点"
	WHEN t1.`hour` >= 5 and t1.`hour` <= 8 THEN "5-8点"
	WHEN t1.`hour` >= 9 and t1.`hour` <= 12 THEN "9-12点"
	WHEN t1.`hour` >= 13 and t1.`hour` <= 16 THEN "13-16点"
	WHEN t1.`hour` >= 17 and t1.`hour` <= 20 THEN "17-20点"
	WHEN (t1.`hour` >= 21 and t1.`hour` <= 23) or (t1.`hour` = 0) THEN "21-24点"
	END) as hour_range,
	SUM(t1.order_count) as order_count,
	SUM(t2.order_count) as yes_order_count,
	SUM(t1.gmv) as gmv,
	SUM(t2.gmv) as yes_gmv
	
FROM
	(
	SELECT
		date(`create_at`) as `day`,
		hour(`create_at`) as `hour`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,`hour`
	)t1 
	LEFT JOIN
	(
	SELECT
		date(`create_at`) as `day`,
		hour(`create_at`) as `hour`,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,`hour`
	) t2
	ON (t1.`day` = DATE_ADD(t2.`day`,interval 1 day)) and (t1.`hour` = t2.`hour`)
GROUP BY
	t1.`day`,hour_range
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
DELETE FROM `dm_pay_mode_percent_month`;
        """,
        'append_table': 'dm_pay_mode_percent_month',
        'data_sql': """
SELECT
	t1.`month`
	,t1.pay_mode
	,t1.pay_mode_count as order_count
	,t1.pay_mode_amount_sum as amount_sum
	,TRUNCATE(t1.pay_mode_count/t2.sum_count,19) as order_count_percent
	,TRUNCATE(t1.pay_mode_amount_sum/t2.sum_amount,19) as amount_sum_percent
FROM
	(
	SELECT
		date_format(`create_at`,"%Y-%m") as `month`
		,pay_mode
		,COUNT(store_num) as pay_mode_count
		,SUM(amount) as pay_mode_amount_sum
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`month`,pay_mode
	) t1
	LEFT JOIN
	(
	SELECT
		date_format(`create_at`,"%Y-%m") as `month`
		,COUNT(store_num) as sum_count
		,sum(amount) as sum_amount
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`month`
	) t2 ON t1.`month` = t2.`month`
    """
    },
    {
        'delete_sql': """
DELETE FROM `unionpay_statistics_day_formats`;
        """,
        'append_table': 'unionpay_statistics_day_formats',
        'data_sql': """
SELECT
	"678" as `id`,
	"id_guangzhou_tianhelu" as circle_id,
	CONCAT("no00",t1.week_num) as week_number,
	IF(t1.week_day = "0","7",t1.week_day) as week_day,
	(CASE 
	WHEN t2.b_type IN ("彩妆护肤","次主力店","家具家电","品牌服饰","珠宝首饰","综合零售") THEN "1"
	WHEN t2.b_type = "美食餐饮" THEN "2"
	WHEN t2.b_type = "休闲运动" THEN "4"
	WHEN t2.b_type = "娱乐体验" THEN "5"
	ELSE "6"
	END) as service_type,
	t1.gmv as tr_amt,
	SUM(t1.order_count) as tr_num,
	0 as tr_card,
	now() as created_time,
	date_format(t1.`day`,"%Y%m%d") as b_date
FROM
	(
	select
		date_format(`create_at`,'%v') as `week_num`,
		date_format(`create_at`,'%w') as `week_day`,
		date(`create_at`) as `day`,
		store_num,
		store_name,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,store_num,store_name
	)t1
	INNER JOIN dm_store_b_type_info t2 
	ON t1.store_num = t2.store_num and t1.store_name = t2.store_name
GROUP BY
	b_date,service_type
	
UNION ALL

SELECT
	"678" as `id`,
	"id_guangzhou_tianhelu" as circle_id,
	CONCAT("no00",t1.week_num) as week_number,
	IF(t1.week_day = "0","7",t1.week_day) as week_day,
	"0" as service_type,
	t1.gmv as tr_amt,
	SUM(t1.order_count) as tr_num,
	0 as tr_card,
	now() as created_time,
	date_format(t1.`day`,"%Y%m%d") as b_date
FROM
	(	
	select
		date_format(`day`,'%v') as `week_num`,
		date_format(`day`,'%w') as `week_day`,
		`day`,
		order_count,
		gmv
	FROM
		dm_order_target_day
	)t1
GROUP BY
	b_date
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
DELETE FROM `dm_business_increase_month`;
        """,
        'append_table': 'dm_business_increase_month',
        'data_sql': """
with t as (
SELECT
	cast(t1.`month` as char) as `month`,
	truncate((ifnull(t1.number_index,0) + ifnull(t2.sum_index,0))*0.4 + ifnull(t3.gmv_index,0)*0.3 + ifnull(t4.sum_index,0)*0.3,18) as `index`
FROM
	(
	SELECT
		`month`,
		number_ring_ratio as number_index
	FROM
		dm_consumer_flow_arrive_month
	WHERE
		source = "all"
		and 
		-- 去除本月数据
		`month` <> date_format(now(),"%Y%m") 
	) t1
	LEFT JOIN
	(
	SELECT
		`month`,
		sum(index_ring_ratio) as sum_index
	FROM
		dm_district_index_month
	WHERE
		source = "all"
		and
		`type` IN ("female","night","youth")
	GROUP BY
		`month`
	) t2 ON CAST(t1.`month` as char) = t2.`month`
	LEFT JOIN
	(
	SELECT
		s1.`month`,
		truncate((s1.gmv-s2.gmv)/s2.gmv,18) as gmv_index
	FROM
		dm_ta_order_target_month s1
		LEFT JOIN
		dm_ta_order_target_month s2 ON str_to_date(CONCAT(s1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(s2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH)
	) t3 ON CAST(t1.`month` as char) = t3.`month`
	LEFT JOIN
	(
	SELECT
		date_format(str_to_date(CONCAT(`month`,'-01'),'%Y-%m-%d'),'%Y%m') as month_2,
		sum(index_ring_ratio) as sum_index
	FROM
		dm_origin_index_percent_month
	WHERE
		source = "all"
		and
		`type` IN ("guangdong_inside","guangdong_outside","guangzhou_inside")
		and
		index_ring_ratio IS NOT NULL
	GROUP BY
		month_2
	)t4 ON CAST(t1.`month` as char) = t4.month_2
)

SELECT
	t1.`month`,
	t1.`index`,
	-- 若除数等于0或者为空，则置0；若除数小于0，则取其绝对值；
	(CASE
	when (t2.`index`=0 or t2.`index` is null) then 0
	when t2.`index`<0 then truncate((t1.`index`-t2.`index`)/(-t2.`index`),18)
	else truncate((t1.`index`-t2.`index`)/t2.`index`,18)
	END) as index_ring_ratio
FROM
	t t1
	LEFT JOIN t t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH)
    """
    }
]
