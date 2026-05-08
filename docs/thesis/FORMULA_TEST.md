# ТЕСТУВАННЯ ВІДОБРАЖЕННЯ ФОРМУЛ (ЕТАП 7 - ШТУРМ)

## Варіант 24: Спеціальний vphantom (силове розтягування)
$$
MAPE = \frac{100}{n} \sum \left| \vphantom{\frac{A}{B}} \frac{y_i - \hat{y}_i}{y_i} \right|
$$

## Варіант 25: Використання подвійних палок (якщо Word ігнорує одну)
$$
MAPE = \frac{100}{n} \sum || \frac{y_i - \hat{y}_i}{y_i} ||
$$

## Варіант 26: Побудова через корінь (Математичний хак для ідеальних палок)
$$
MAPE = \frac{100}{n} \sum \sqrt{ \left( \frac{y_i - \hat{y}_i}{y_i} \right)^2 }
$$

## Варіант 27: Використання \vert замість |
$$
MAPE = \frac{100}{n} \sum \left\vert \frac{y_i - \hat{y}_i}{y_i} \right\vert
$$

## Варіант 28: Масштабування через Bigm
$$
MAPE = \frac{100}{n} \sum \Bigm| \frac{y_i - \hat{y}_i}{y_i} \Bigm|
$$

## Варіант 29: RMSE через поєднання \displaystyle та \sqrt
$$
RMSE = \displaystyle \sqrt{ \frac{1}{n} \sum (y_i - \hat{y}_i)^2 }
$$

## Варіант 30: MAPE через масив 1x1 (змушує Word малювати високі палки)
$$
MAPE = \frac{100}{n} \sum \left| \begin{array}{c} \frac{y_i - \hat{y}_i}{y_i} \end{array} \right|
$$
