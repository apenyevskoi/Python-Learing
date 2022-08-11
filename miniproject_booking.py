# This is learning miniproject using booking dataset and providing the simple analysing
#PANDAS

import pandas as pd

df = pd.read_csv('bookings.csv', sep = ';')
df = df.rename(columns = {
'Hotel' : 'hotel',
'Is Canceled' : 'is_canceled',
'Lead Time' :'lead_time',
'arrival full date' : 'arrival_full_date',
'Arrival Date Year' : 'arrival_date_year',
'Arrival Date Month' : 'arrival_date_month',
'Arrival Date Week Number' : 'arrival_date_week_number',
'Arrival Date Day of Month' : 'arrival_date_day_of_month',
'Stays in Weekend nights' : 'stays_in_weekend_nights',
'Stays in week nights' :'stays_in_week_nights',
'stays total nights' :'stays_total_nights',
'Adults' : 'adults',
'Children' : 'children',
'Babies' : 'babies',
'Meal' : 'meal',
'Country' : 'country',
'Reserved Room Type' :'reserved_room_type',
'Assigned room type' :'assigned_room_type',
'customer type' :'customer_type',
'Reservation Status' :'reservation_status',
'Reservation status_date' : 'reservation_status_date'})

# QUERIES
#1
get_most_popular_countries = df \
    .query("is_canceled == 0") \
    .groupby(by = ['country', 'reservation_status'], as_index = False) \
    .agg({'reservation_status' : 'count'}) \
    .rename(columns = {'reservation_status' : 'count of check-outs'}) \
    .sort_values('count of check-outs', ascending = False)[:5]
print(f'Most popular countries are \n{get_most_popular_countries}\n')

#2
av_tot_nights = df \
    .groupby(by = ['hotel']) \
    .agg({'stays_total_nights' : 'mean'}) \
    .rename(columns = {'stays_total_nights' : 'average total nights'})
print(f'Average used total nights\n{av_tot_nights}\n')

#3
diff_bw_reserv_assign = len(df[(df['reserved_room_type'] != df['assigned_room_type'])])
print(f'\nDifference between reserved and assigned bookings, total \n {diff_bw_reserv_assign}')

#4
super_month_2016 = df[df['arrival_date_year'] == 2016] \
    .query("reservation_status == 'Check-Out'") \
    .groupby('arrival_date_month') \
    .agg({'arrival_date_month' : 'count'}) \
    .idxmax()[0]
max_value_month_2016 = df[df['arrival_date_year'] == 2016] \
    .query("reservation_status == 'Check-Out'") \
    .groupby('arrival_date_month') \
    .agg({'arrival_date_month' : 'count'}).max()[0]
super_month_2017 = df[(df['arrival_date_year'] == 2017)] \
    .query("reservation_status == 'Check-Out'") \
    .groupby('arrival_date_month') \
    .agg({'arrival_date_month' : 'count'}) \
    .idxmax()[0]
max_value_month_2017 = df[df['arrival_date_year'] == 2017] \
    .query("reservation_status == 'Check-Out'") \
    .groupby('arrival_date_month') \
    .agg({'arrival_date_month' : 'count'}).max()[0]
print(f'\nMost success months in 2016 and 2017 \n {super_month_2016} ({max_value_month_2016} check-outs) and {super_month_2017} ({max_value_month_2017} check-outs)\n')

#5
cancelation_city_hotel = df[(df['hotel'] == 'City Hotel')][lambda x: x['is_canceled'] == 1] \
    .groupby(['arrival_date_year', 'arrival_date_month']) \
    .agg({'arrival_date_year' : 'count'}) \
    .rename(columns = {'arrival_date_year' : 'count of cancelation'})
print(f'\nBooking cancelation in City Hotel type \n {cancelation_city_hotel} \n')

#6
max_mean_val = df[['adults','children', 'babies']].mean().max()
type_of_guest = df[['adults','children', 'babies']].mean().idxmax()
print(f'\nThe most mean value among guests type {type_of_guest} is {max_mean_val}')

#7
df['total_kids'] = df['children'] + df['babies']
df.groupby('hotel').agg({'total_kids' : 'sum'})
av_child_booking = df[['hotel', 'total_kids']].groupby('hotel').mean().rename(columns = {'total_kids' : 'count of children per booking'})
print(f'\nAverage count of booking with children\n {av_child_booking}')

#8
df['has_kids'] = df['total_kids'] > 0
tmp = df.groupby(['is_canceled', 'has_kids'], as_index = False).agg({'has_kids' : 'count'})
ratio_cancel_without_child = (tmp['has_kids'].loc[2] / (tmp['has_kids'].loc[0] + tmp['has_kids'].loc[2])) * 100
ratio_cancel_with_child = (tmp['has_kids'].loc[3] / (tmp['has_kids'].loc[1] + tmp['has_kids'].loc[3])) * 100
print(f'\nRatio of cancelation without children {ratio_cancel_without_child.round(2)}%\n')
print(f'Ratio of cancelation with children {ratio_cancel_with_child.round(2)}%\n')