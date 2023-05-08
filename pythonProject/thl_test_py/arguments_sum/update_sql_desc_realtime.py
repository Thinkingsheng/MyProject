# -*- coding:utf-8 -*-

# 需实时更新的数据
realtime_update = [
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
DELETE FROM `dm_total_member_visiter_count`;
    """,
        'append_table': 'dm_total_member_visiter_count',
        'data_sql': """
SELECT
	ref_date as `day`,
	sum(visit_uv_new) over(order by ref_date) as total_member,
	sum(visit_uv) over(order by ref_date) as total_visiter
FROM
	wechat_mini_visit_trend_analysis
WHERE
	char_length(ref_date)=8
    """
    }
]