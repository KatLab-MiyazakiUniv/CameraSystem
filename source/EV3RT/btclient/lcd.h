#ifndef LCD_H_
#define LCD_H_

void init_lcd();
void lcd_reset();
void term_lcd();
void lcd_print(char *format, ...);

#endif /* LCD_H_ */
