#include "highpass.h"

#include<qfont.h>
#include<stdio.h>


Highpass::Highpass() : QComboBox() {

	dcValue = 0;

	setMinimumWidth ( fontMetrics().width("1000Hz_") );

	addItem(tr("off"),-1);
	addItem(tr("-DC"),0);
	addItem(tr("0.1Hz"),1);
	addItem(tr("0.2Hz"),2);
	addItem(tr("0.5Hz"),5);
	addItem(tr("1Hz"),10);
	addItem(tr("2Hz"), 20);
	addItem(tr("5Hz"), 50);
	addItem(tr("10Hz"),100);

	connect(this,
		SIGNAL( activated(int) ),
		this,
		SLOT( setFrequencyIndex(int) ) );

	setCurrentIndex(0);
}

void Highpass::setFrequencyIndex ( int index ) {
 	frequency = itemData(index).toFloat()/10.0;
	if (frequency > 0) {
		hp.setup(samplingrate,
			 (float)frequency);
		//_RPT1(0, "Highpass cutoff: %f Hz\n", frequency);
	}
}

void Highpass::setFrequency(float f) {
	int index = findData(((int)(f * 10)));
	if (index != -1) {
		setCurrentIndex(index);
		setFrequencyIndex(index);
	}
}


float Highpass::filter(float v) {
	if (dcCtr > 0) {
		dcValue = dcValue + (v - dcValue) / INERTIA_FOR_DC_DETECTION;
		dcCtr--;
	}
	if (frequency == 0) {
		v = v - dcValue;
		return v;
	}
	dcCtr = samplingrate;
	if (frequency > 0) {
		return hp.filter(v);
	}
	return v;
}
