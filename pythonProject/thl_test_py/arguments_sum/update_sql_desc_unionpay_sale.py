# -*- coding:utf-8 -*-

# 需实时更新的数据
unionpay_sale_update = [
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
