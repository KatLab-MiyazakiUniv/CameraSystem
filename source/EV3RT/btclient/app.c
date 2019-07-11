#include <stdio.h>
#include <stdlib.h>
#include "ev3api.h"
#include "app.h"
#include "lcd.h"

//#define DEBUG_PRINT

#define error( fmt, ... ) \
	lcd_print( \
		"<Err> " fmt "\n", ##__VA_ARGS__ \
	)

#ifndef DEBUG_PRINT
#define debug( fmt, ... ) ((void)0)
#else /* DEBUG_PRINT */
#define debug( fmt, ... ) lcd_print( fmt, ##__VA_ARGS__ )
#endif

static const int TOUCH_SENSOR_PORT = EV3_PORT_1;

/* 色コードの定義 */
enum EColor {
	eUnknown = 0,
	eRed = 1,
	eGreen = 2,
	eBlue = 3,
	eBlack = 4,
	eYellow = 5,
	eColorMax // must be at last
};

/* コマンドコードの定義 */
enum ECommandCode {
	eSpecific = 0x01,
	eAll = 0x02
};

/* レスポンスコードの定義 */
enum EResCode {
	eColor = 0x51,
	eError = 0xc8
};

/* 座標IDと色のセットを表す構造体 */
typedef struct PointColor_st {
	uint16_t point;
	enum EColor color;
} PointColor;

/* 色コードを文字列化する関数 */
static char* color2str( enum EColor col )
{
	static struct {
		enum EColor color;
		char *displayStr;
	} colorStr[] = {
		{eUnknown, "Unknown"}, 
		{eRed, "Red"}, 
		{eGreen, "Green"}, 
		{eBlue, "Blue"}, 
		{eBlack, "Black"}, 
		{eYellow, "Yellow"}
	};
	size_t i = 0;

	for ( i = 0; i < eColorMax; i++ ) {
		if ( colorStr[i].color == col ) {
			return colorStr[i].displayStr;
		}
	}
	return "";
}

/* コマンド(要求)パケット生成関数 */
static size_t encode_packet(uint8_t reqcode, uint16_t points[], size_t num_of_points, uint8_t **packet)
{
	uint8_t *data = NULL;
	size_t l_num_of_points = 0;
	size_t l_parameter_length = 0;
	size_t packet_size = 0;
	size_t packet_index = 0;
	size_t i = 0;

	if ( (packet == NULL) || ((reqcode != eSpecific) && (reqcode != eAll)) || (num_of_points > 84) ) {
		error("invalid argument");
		return 0;
	}

	if ( reqcode == eSpecific ) {
		l_num_of_points = num_of_points;
		l_parameter_length = 1/* 座標数 */ + sizeof(uint16_t)*l_num_of_points/* 座標ID */;
	}

	packet_size = 1/* Command Code */ + 1/* Parameter Length */ + l_parameter_length;
	data = (uint8_t *)malloc( packet_size );
	if ( data == NULL ) {
		error("failed to malloc");
		return 0;
	}
	
	/* command code */
	data[packet_index++] = reqcode;
	
	/* parameter length */
	data[packet_index++] = l_parameter_length;
	
	/* parameter */
	if ( reqcode == eSpecific ) {
		data[packet_index++] = l_num_of_points;
		for ( i = 0; i < l_num_of_points; i++, packet_index = packet_index + 2 ) {
			/* into network byte order */
			data[packet_index] = (uint8_t) ((points[i] & 0xF0) >> 8);
			data[packet_index+1] = (uint8_t) (points[i] & 0x0F);
		}
	}

	*packet = data;

	return packet_size;
}

static int decode_packet(uint8_t rescode, uint8_t *data, size_t data_len, PointColor **result, size_t *num_of_result, char **errmsg)
{
	size_t num_of_points = 0;
	PointColor *l_result = NULL;
	char *l_errmsg = NULL;
	size_t i = 0;
	size_t data_index = 0;

	if ( ((rescode != eColor) && (rescode != eError)) || (data == NULL) ) {
		error("invalid argument");
		return -1;
	}
	
	if ( rescode == eColor ) {
		if ( (result == NULL) || (num_of_result == NULL) ) {
			error("invalid argument");
			return -1;
		}
		num_of_points = (size_t)data[data_index++];
		l_result = (PointColor *)malloc(sizeof(PointColor)*num_of_points);
		if ( l_result == NULL ) {
			error("failed to malloc");
			return -1;
		}
		for ( i = 0; i < num_of_points; i++, data_index = data_index + 3 ) {
			l_result[i].point = ((uint16_t)data[data_index] << 8) + (uint16_t)data[data_index+1]; /* from network byte order */
			l_result[i].color = data[data_index+2];
		}
	} else if ( rescode == eError ) {
		if ( errmsg == NULL ) {
			error("invalid argument");
			return -1;
		}
		l_errmsg = (char *)calloc(data_len+1, sizeof(uint8_t));
		for ( i = 0; i < data_len; i++ ) {
			l_errmsg[i] = (char)data[i];
		}
	}

	*result = l_result;
	*num_of_result = num_of_points;
	*errmsg = l_errmsg;

	return 0;
}

static FILE *serial_open()
{
	FILE *bt = NULL;

	bt = ev3_serial_open_file(EV3_SERIAL_BT);
	if ( bt == NULL ) {
		error("failed to ev3_serial_open_file");
		return NULL;
	}

	return bt;
}

static int serial_write(FILE *bt, uint8_t *data, size_t data_len)
{
	if ( (bt == NULL) || (data == NULL) ) {
		error("invalid argument");
		return -1;
	}

	if ( fwrite(data, 1, data_len, bt) < data_len ) {
		error("failed to fwrite");
		return -1;
	}

	return 0;
}

static int serial_read(FILE *bt, uint8_t *code, uint8_t **data, size_t *data_len)
{
	uint8_t l_code;
	uint8_t l_data_len;
	uint8_t *l_data = NULL;

	if ( (bt == NULL) || (code == NULL) || (data == NULL) || (data_len == NULL) ) {
		error("invalid argument");
		return -1;
	}

	if ( fread(&l_code, sizeof(uint8_t), 1, bt) < 1 ) {
		error("failed to fread [code]");
		return -1;
	}
	
	if ( fread(&l_data_len, sizeof(uint8_t), 1, bt) < 1 ) {
		error("failed to fread [datalen]");
		return -1;
	}

	l_data = (uint8_t *)malloc(l_data_len);
	if ( l_data == NULL ) {
		error("failed to malloc");
		return -1;
	}
	if ( fread(l_data, sizeof(uint8_t), l_data_len, bt) < l_data_len ) {
		error("failed to fread [data]");
		free(l_data);
		return -1;
	}

	*code = l_code;
	*data_len = l_data_len;
	*data = l_data;

	return 0;
}

void main_task(intptr_t unused)
{
	int ret = -1;
	FILE *bt = NULL;
	uint8_t *request = NULL;
	size_t request_len = 0;
	uint8_t rescode;
	uint8_t *response = NULL;
	size_t response_len = 0;
	uint16_t points[] = { 1, 2, 3 }; /* 要求する座標IDの配列 */
	PointColor *result = NULL;
	size_t num_of_result = 0;
	char *errmsg = NULL;
	size_t i = 0;

	init_lcd();
	
	lcd_print("program start.\n");

	// タッチセンサを設定
	ev3_sensor_config(TOUCH_SENSOR_PORT, TOUCH_SENSOR);

	// Bluetooth通信を開通
	bt = serial_open();
	if ( bt == NULL ) {
		error("failed to serial_open");
		goto end;
	}
	lcd_print("bluetooth connected.\n");

	// タッチセンサ押下待ち
	lcd_print("Press the touch sensor.\n");
    while(!ev3_touch_sensor_is_pressed(TOUCH_SENSOR_PORT));
    while(ev3_touch_sensor_is_pressed(TOUCH_SENSOR_PORT));

	// 色判定リクエストメッセージを生成
	request_len = encode_packet(eSpecific, points, sizeof(points)/sizeof(points[0]), &request); /* 座標IDを指定する場合 */
	//request_len = encode_packet(eAll, NULL, 0, &request); /* すべての座標IDの色を取得する場合 */
	if ( request_len == 0 ) {
		error("failed to encode_packet");
		goto end;
	}
	debug("req = ");
	for ( i = 0; i < request_len; i++ ) {
		debug("%02x", request[i]);
	}
	debug("\n");
	
	// メッセージを送信
	ret = serial_write(bt, request, request_len);
	if ( ret != 0 ) {
		error("failed to serial_write");
		goto end;
	}

	// 応答を受信
	ret = serial_read(bt, &rescode, &response, &response_len);
	if ( ret != 0 ) {
		error("failed to serial_read");
		goto end;
	}
	debug("rescode = %u\n", rescode);
	debug("resdata = ");
	for ( i = 0; i < response_len; i++ ) {
		debug("%02x", response[i]);
	}
	debug("\n");

	// 応答メッセージを解読
	ret = decode_packet(rescode, response, response_len, &result, &num_of_result, &errmsg);
	if ( ret != 0 ) {
		error("failed to decode_packet");
		goto end;
	}
	
	// 色判定結果をLCDへ出力
	for ( i = 0; i < num_of_result; i = i + 2 ) {
		lcd_print("(%u, %s)", result[i].point, color2str(result[i].color));
		if ( i+1 < num_of_result ) {
			lcd_print(" (%u, %s)", result[i+1].point, color2str(result[i+1].color));
		}
		lcd_print("\n");
	}
	if ( errmsg != NULL ) {
		lcd_print("errmsg = %s\n", errmsg);
	}

end:
	if ( bt != NULL ) {
		fclose(bt);
		lcd_print("bluetooth disconnected.\n");
	}
	if ( request != NULL ) {
		free(request);
	}
	if ( response != NULL ) {
		free(response);
	}
	if ( result != NULL ) {
		free(result);
	}
	if ( errmsg != NULL ) {
		free(errmsg);
	}
	
	lcd_print("program end.\n");
	
	term_lcd();

	return;
}
