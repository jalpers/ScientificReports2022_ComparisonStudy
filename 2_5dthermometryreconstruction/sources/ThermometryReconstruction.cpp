#include "ThermometryReconstruction.h"
#include "ui_ThermometryReconstruction.h"
#include <DicomHandler.h>
#include<CoordinatesConverter.h>
//#include<InterpolationMap.h>

#include <time.h>
#include<vtkImageData.h>
ThermometryReconstruction::ThermometryReconstruction(QWidget *parent)
	: QMainWindow(parent)
	, ui(new Ui::ThermometryReconstruction)
{
	ui->setupUi(this);
	/*
	*	Set default value for file path.
	*/
	ui->q_lineEdit_filename->setText("Path/Phantome/");
	
	/*
	*	Initialize members.
	*/
	m_necrosisMapComputation = new NecrosisMapComputation();
	isCropped = true;

	/*
	*	Connect signals.
	*/
	timer = new QTimer(this);
	fileID = 0;
	connect(timer, SIGNAL(timeout()), this, SLOT(updateImage()));
	QObject::connect(ui->q_pushButton_browse, SIGNAL(clicked()), this, SLOT(slotButtonBrowse()));
	QObject::connect(ui->q_pushButton_defineReference, SIGNAL(clicked()), this, SLOT(slotButtonDefineReference()));
	QObject::connect(ui->q_pushButton_computeHeatMap, SIGNAL(clicked()), this, SLOT(slotButtonComputeHeatMap()));
}

ThermometryReconstruction::~ThermometryReconstruction()
{
	delete ui;
}
void ThermometryReconstruction::updateImage()
{
	qDebug() << "New Slice -> Update Volume";

	vtkSmartPointer<vtkRenderWindow> q_vtk_renderWindow_Right = vtkSmartPointer<vtkRenderWindow>::New();
	q_vtk_renderWindow_Right = ui->q_vtk_viewerRight->GetRenderWindow();

	vtkSmartPointer<vtkRenderWindow> q_vtk_renderWindow_Left = vtkSmartPointer<vtkRenderWindow>::New();
	q_vtk_renderWindow_Left = ui->q_vtk_viewerLeft->GetRenderWindow();

	volume.addSlice(angleList[fileID], QString::fromStdString((std::to_string(timestep))));
	
	volume.display(q_vtk_renderWindow_Right, isCropped);
	volume.display(q_vtk_renderWindow_Left, isCropped, true);
	volume.interpolate(inPo.getinterpolationMap2D(), inPo.getVesselMap());
	fileID++;
	qDebug() << fileID << "id";
	if (fileID >= angleList.size())
	{	
		timestep++;
		fileID = 0;
		qDebug() << fileID << "id"<<timestep <<"step";

	}
	if (timestep >= 15)
	{
		timer->stop();
	}
		
		//
		//volume.display(q_vtk_renderWindow_Left, isCropped);
		////m_necrosisMapComputation->computeHeatMap(referenceVolume.getImageData(), volume.getImageData(), volume.getImageData(), 1.5, 9.56);
		//volume.display(q_vtk_renderWindow_Right, isCropped);
	
	

}
/************************************************************************************
*								    slotButtonBrowse
*************************************************************************************/
void ThermometryReconstruction::slotButtonBrowse()
{
	/*
	*	Open file browser to specify file and set the text field.
	*/

	QString q_c_filename = m_q_dialog->getExistingDirectory();
	//QString q_c_filename = m_q_dialog->getOpenFileName();

	ui->q_lineEdit_filename->setText(q_c_filename);
}
/************************************************************************************
*								    slotButtonDefineReference
*************************************************************************************/
void ThermometryReconstruction::slotButtonDefineReference()
{
	/*
	*	Open file browser to specify file and set the text field.
	*/


	vtkSmartPointer<vtkRenderWindow> q_vtk_renderWindow_Left = vtkSmartPointer<vtkRenderWindow>::New();

	q_vtk_renderWindow_Left = ui->q_vtk_viewerLeft->GetRenderWindow();



	//q_c_dicomFilePath = ui->q_lineEdit_filename->text();
	QString l = ui->q_lineEdit_filename->text();
	QString lastStep = "lastStep";
	QString delimeter = "/";
	for (int i = 0; i< phantoms.size(); i++)
	{
		foreach(const QString &neko, nekos)
		{
			q_c_dicomFilePath = l +  phantoms.at(i)+ delimeter + "HeatMap" + delimeter + lastStep + delimeter + neko;
			qDebug() << q_c_dicomFilePath;
			referenceVolume = DataVolume(q_c_dicomFilePath);


			//InterpolationMap inPo;
			//inPo = InterpolationMap(referenceVolume.getWorld2VoxelConverter());
			//inPo.populateInterpolationMap(q_c_dicomFilePath);




			for (int t = 13; t <= 13; t++)
			{
				for (int i = 0; i < angleList.size(); i++)//
				{
					referenceVolume.addSlice(angleList[i], QString::fromStdString((std::to_string(t))));
				}
			}

			referenceVolume.display(q_vtk_renderWindow_Left, false);


			referenceVolume.writeToFile(QString(q_c_dicomFilePath));


			/*if (q_c_dicomFilePath.contains(new QString("Perfusion")))
			{
				qDebug() << "isPerfusion";
				inPo.loadVesselMap(tubeFilePath);
			}*/


			//referenceVolume.interpolate(inPo.getinterpolationMap2D(),inPo.getVesselMap());
			//
			//
			//referenceVolume.writeToFile(q_c_dicomFilePath + "/lol");
			//referenceVolume.display(q_vtk_renderWindow_Left, false);

		}
		
	}

	
}
/************************************************************************************
*								    slotButtonComputeHeatMap
*************************************************************************************/
void ThermometryReconstruction::slotButtonComputeHeatMap()
{

	
	vtkSmartPointer<vtkDICOMImageReader> _reader = vtkSmartPointer<vtkDICOMImageReader>::New();
	q_c_dicomFilePath = ui->q_lineEdit_filename->text();
	volume = DataVolume(q_c_dicomFilePath);


	inPo = InterpolationMap(volume.getWorld2VoxelConverter());
	inPo.populateInterpolationMap(q_c_dicomFilePath);
	
	if (q_c_dicomFilePath.contains(new QString("Perfusion")))
	{
		qDebug() << "isPerfusion";
		inPo.loadVesselMap(tubeFilePath);
	}


	fileID = 0;
	timestep = 1;
	qDebug() << "timer->start";
	timer->start(1000);


	
	
}






