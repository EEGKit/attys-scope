#include "lowpass.h"

#include<qfont.h>
#include<stdio.h>


Lowpass::Lowpass() : QComboBox() {

	addItem(tr("off"),0);
	addItem(tr("1Hz"), 1);
	addItem(tr("2Hz"), 2);
	addItem(tr("5Hz"), 5);
	addItem(tr("10Hz"),10);
	addItem(tr("20Hz"), 20);
	addItem(tr("50Hz"), 50);
	addItem(tr("||1Hz"), -1);
	addItem(tr("||2Hz"), -2);
	addItem(tr("||5Hz"), -5);

	connect(this,
		SIGNAL( activated(int) ),
		this,
		SLOT( setFrequencyIndex(int) ) );

	setCurrentIndex(0);
}

void Lowpass::setFrequencyIndex ( int index ) {
 	frequency = (float)(itemData(index).toFloat());
	if (fabs(frequency) > 0) {
		lp.setup(samplingrate,
			 (float)fabs(frequency));
	}
}

void Lowpass::setFrequency(float f) {
	//_RPT1(0, "setFre lowpass=%fHz\n", f);
	int index = findData(f);
	if (index != -1) {
		setCurrentIndex(index);
		setFrequencyIndex(index);
	}
}

float Lowpass::filter(float v) {
	if (frequency > 0) {
		return lp.filter(v);
	}
	else {
		if (frequency < 0) {
			return lp.filter(fabs(v));
		}
	}
	return v;
}
