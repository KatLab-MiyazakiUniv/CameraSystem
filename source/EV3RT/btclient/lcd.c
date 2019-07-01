#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include "ev3api.h"

static int is_initialized = 0;
static char *buffer = NULL;
static int32_t width = 0;
static int32_t height = 0;
static int curr_x = 0;
static int curr_y = 0;
static int MAX_LINE_NUM = 0;

void init_lcd() {
	if ( is_initialized ) {
		return;
	}
	ev3_lcd_set_font(EV3_FONT_SMALL);
	ev3_font_get_size(EV3_FONT_SMALL, &width, &height);
	MAX_LINE_NUM = EV3_LCD_HEIGHT/height;
	buffer = calloc(1, EV3_LCD_WIDTH/width+1);
	is_initialized = 1;
}

void lcd_reset() {
	curr_x = 0;
	curr_y = 0;
}

void term_lcd() {
	free(buffer);
	is_initialized = 0;
}

static void lcd_draw_string(const char *str) {
	char spaces[EV3_LCD_WIDTH/width+1];
	char out_str[EV3_LCD_WIDTH/width+1];
	size_t i, str_index = 0;
	int nl_flag = 0;

	memset(spaces, ' ', EV3_LCD_WIDTH/width);
	spaces[EV3_LCD_WIDTH/width] = '\0';
	memset(out_str, 0x00, EV3_LCD_WIDTH/width+1);

	while( str_index < strlen(str) ) {
		memset(out_str, 0x00, EV3_LCD_WIDTH/width+1);
		for ( i = 0; str[str_index] != '\0'; i++, str_index++  ) {
			if ( str[str_index] == '\n' ) {
				str_index++;
				nl_flag = 1;
				break;
			}
			if ( i < EV3_LCD_WIDTH/width ) {
				out_str[i] = str[str_index];
			}
		}
		if ( curr_x < EV3_LCD_WIDTH ) {
			if ( curr_x == 0 ) {
				ev3_lcd_draw_string(spaces, 0, curr_y);
			}
			ev3_lcd_draw_string(out_str, curr_x, curr_y);
			curr_x = (curr_x + strlen(out_str)*width) > EV3_LCD_WIDTH ? EV3_LCD_WIDTH : (curr_x + strlen(out_str)*width);
		}
		if ( nl_flag ) {
			if ( (curr_y + height) < (MAX_LINE_NUM * height) ) {
				curr_y += height;
				curr_x = 0;
			} else {
				curr_y = 0;
				curr_x = 0;
			}
			nl_flag = 0;
		}
	}
}

void lcd_print(char *format, ...) {
	va_list args;
	int size = 0;
	char *tmp = NULL;

	va_start(args , format);

	size = vprintf(format, args);
	if ( size <= 0 ) {
		return;
	}
	tmp = (char *)calloc(1, size+1);
	if ( tmp == NULL ) {
		return;
	}
	vsprintf(tmp, format, args);

	memset(buffer, 0x00, EV3_LCD_WIDTH/width+1);
	vsnprintf(buffer, EV3_LCD_WIDTH/width, format, args);

	va_end(args);
	
	lcd_draw_string(buffer);
	if ( (size >= EV3_LCD_WIDTH/width) && (tmp[size-1] == '\n') ) {
		lcd_draw_string("\n");
	}

	free(tmp);

	return;
}
