from datetime import datetime


REPORT_TYPES = {'summary', 'detailed', 'forecast'}
OUTPUT_FORMATS = {'pdf', 'excel', 'html', 'json'}


def generate_sales_report(sales_data, report_type='summary', date_range=None,
                         filters=None, grouping=None, include_charts=False,
                         output_format='pdf'):
    """Generate a sales report while preserving the original public API."""
    validate_report_request(sales_data, report_type, output_format, date_range)
    filtered_sales = filter_sales_data(sales_data, date_range, filters)

    if not filtered_sales:
        print("Warning: No data matches the specified criteria")
        if output_format == 'json':
            return {"message": "No data matches the specified criteria", "data": []}
        return _generate_empty_report(report_type, output_format)

    grouped_data = group_sales_data(filtered_sales, grouping)
    report_data = build_base_report(
        filtered_sales, report_type, date_range, filters, grouping, grouped_data
    )
    add_report_type_details(report_data, report_type, filtered_sales)
    add_grouping_details(report_data, grouping, grouped_data, sum_sales(filtered_sales))

    if include_charts:
        report_data['charts'] = build_charts(filtered_sales, grouping, grouped_data)

    return render_report(report_data, output_format, include_charts)


def validate_report_request(sales_data, report_type, output_format, date_range):
    """Validate the input values required to build a sales report."""
    if not sales_data or not isinstance(sales_data, list):
        raise ValueError("Sales data must be a non-empty list")
    if report_type not in REPORT_TYPES:
        raise ValueError("Report type must be 'summary', 'detailed', or 'forecast'")
    if output_format not in OUTPUT_FORMATS:
        raise ValueError("Output format must be 'pdf', 'excel', 'html', or 'json'")
    if date_range:
        validate_date_range(date_range)


def validate_date_range(date_range):
    """Validate that a date range has ordered ISO-formatted endpoints."""
    if 'start' not in date_range or 'end' not in date_range:
        raise ValueError("Date range must include 'start' and 'end' dates")
    start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
    end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")


def filter_sales_data(sales_data, date_range=None, filters=None):
    """Return sales matching the optional date range and field filters."""
    filtered_sales = list(sales_data)
    if date_range:
        start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
        end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')
        filtered_sales = [
            sale for sale in filtered_sales
            if start_date <= datetime.strptime(sale['date'], '%Y-%m-%d') <= end_date
        ]
    for key, expected_value in (filters or {}).items():
        if isinstance(expected_value, list):
            filtered_sales = [
                sale for sale in filtered_sales if sale.get(key) in expected_value
            ]
        else:
            filtered_sales = [
                sale for sale in filtered_sales if sale.get(key) == expected_value
            ]
    return filtered_sales


def sum_sales(sales_data):
    """Return the total amount represented by sales transactions."""
    return sum(sale['amount'] for sale in sales_data)


def calculate_summary(sales_data):
    """Calculate the aggregate metrics shared by all report types."""
    total_sales = sum_sales(sales_data)
    maximum_sale = max(sales_data, key=lambda sale: sale['amount'])
    minimum_sale = min(sales_data, key=lambda sale: sale['amount'])
    return {
        'total_sales': total_sales,
        'transaction_count': len(sales_data),
        'average_sale': total_sales / len(sales_data),
        'max_sale': summarize_sale(maximum_sale),
        'min_sale': summarize_sale(minimum_sale),
    }


def summarize_sale(sale):
    """Return the summary representation for one sale."""
    return {'amount': sale['amount'], 'date': sale['date'], 'details': sale}


def group_sales_data(sales_data, grouping):
    """Group sales by the requested field and calculate group averages."""
    if not grouping:
        return {}
    grouped_data = {}
    for sale in sales_data:
        group_key = sale.get(grouping, 'Unknown')
        group = grouped_data.setdefault(
            group_key, {'count': 0, 'total': 0, 'items': []}
        )
        group['count'] += 1
        group['total'] += sale['amount']
        group['items'].append(sale)
    for group in grouped_data.values():
        group['average'] = group['total'] / group['count']
    return grouped_data


def build_base_report(sales_data, report_type, date_range, filters, grouping,
                      grouped_data):
    """Build the report fields common to every report type."""
    del grouping, grouped_data
    return {
        'report_type': report_type,
        'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': date_range,
        'filters': filters,
        'summary': calculate_summary(sales_data),
    }


def add_report_type_details(report_data, report_type, sales_data):
    """Apply the strategy selected by the report type."""
    report_strategies = {
        'detailed': add_detailed_transactions,
        'forecast': add_forecast_details,
    }
    strategy = report_strategies.get(report_type)
    if strategy:
        strategy(report_data, sales_data)


def add_detailed_transactions(report_data, sales_data):
    """Add transaction details and calculated financial fields."""
    report_data['transactions'] = []
    for sale in sales_data:
        transaction = dict(sale)
        if 'tax' in sale and 'amount' in sale:
            transaction['pre_tax'] = sale['amount'] - sale['tax']
        if 'cost' in sale and 'amount' in sale:
            transaction['profit'] = sale['amount'] - sale['cost']
            transaction['margin'] = (transaction['profit'] / sale['amount']) * 100
        report_data['transactions'].append(transaction)


def add_forecast_details(report_data, sales_data):
    """Add monthly totals, growth rates, and three projected months."""
    monthly_sales = {}
    for sale in sales_data:
        sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        month_key = f"{sale_date.year}-{sale_date.month:02d}"
        monthly_sales[month_key] = monthly_sales.get(month_key, 0) + sale['amount']

    sorted_months = sorted(monthly_sales)
    growth_rates = []
    for previous_month, current_month in zip(sorted_months, sorted_months[1:]):
        previous_total = monthly_sales[previous_month]
        if previous_total > 0:
            growth_rates.append(
                ((monthly_sales[current_month] - previous_total) / previous_total) * 100
            )
    average_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    projected_sales = {}
    if sorted_months:
        year, month = map(int, sorted_months[-1].split('-'))
        last_amount = monthly_sales[sorted_months[-1]]
        for _ in range(3):
            month += 1
            if month > 12:
                month = 1
                year += 1
            forecast_month = f"{year}-{month:02d}"
            last_amount *= 1 + (average_growth_rate / 100)
            projected_sales[forecast_month] = last_amount

    report_data['forecast'] = {
        'monthly_sales': monthly_sales,
        'growth_rates': {
            month: growth_rates[index - 1]
            for index, month in enumerate(sorted_months)
            if index > 0
        },
        'average_growth_rate': average_growth_rate,
        'projected_sales': projected_sales,
    }


def add_grouping_details(report_data, grouping, grouped_data, total_sales):
    """Add group totals and percentages when grouping is requested."""
    if not grouping:
        return
    report_data['grouping'] = {
        'by': grouping,
        'groups': {
            key: {
                'count': group['count'],
                'total': group['total'],
                'average': group['average'],
                'percentage': (group['total'] / total_sales) * 100,
            }
            for key, group in grouped_data.items()
        },
    }


def build_charts(sales_data, grouping, grouped_data):
    """Build chart-ready data for daily sales and optional group totals."""
    date_sales = {}
    for sale in sales_data:
        date_sales[sale['date']] = date_sales.get(sale['date'], 0) + sale['amount']
    dates = sorted(date_sales)
    charts = {
        'sales_over_time': {
            'labels': dates,
            'data': [date_sales[date] for date in dates],
        }
    }
    if grouping:
        charts[f'sales_by_{grouping}'] = {
            'labels': list(grouped_data),
            'data': [group['total'] for group in grouped_data.values()],
        }
    return charts


def render_report(report_data, output_format, include_charts):
    """Select and execute the renderer for the requested output format."""
    renderers = {
        'json': lambda: report_data,
        'html': lambda: _generate_html_report(report_data, include_charts),
        'excel': lambda: _generate_excel_report(report_data, include_charts),
        'pdf': lambda: _generate_pdf_report(report_data, include_charts),
    }
    return renderers[output_format]()


def _generate_empty_report(report_type, output_format):
    """Return the placeholder result for unsupported file renderers."""
    del report_type, output_format
    return None


def _generate_html_report(report_data, include_charts):
    """Placeholder for HTML rendering."""
    del report_data, include_charts
    return None


def _generate_excel_report(report_data, include_charts):
    """Placeholder for Excel rendering."""
    del report_data, include_charts
    return None


def _generate_pdf_report(report_data, include_charts):
    """Placeholder for PDF rendering."""
    del report_data, include_charts
    return None
