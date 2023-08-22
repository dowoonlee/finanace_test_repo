import numpy as np
from datetime import datetime
from data_loader import getData
import matplotlib.pyplot as plt

company = "TSLA"
end = datetime.now()
start = datetime(end.year-10, end.month, end.day)
df = getData(
    company=company,
    start = start,
    end = end)

