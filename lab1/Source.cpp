#define _USE_MATH_DEFINES
#include <windows.h>
#include <stdio.h>
#include <math.h>
#include "fftw3.h"


#define FFT_POINTS 1000
#define FFT_POINTS2 ((double)FFT_POINTS * (double)FFT_POINTS)
#define FS 1.0E+6

const double F = 10000; // Frequency of the input signal
const double DT = 1.0 / FS; // Sampling interval
const double DF = FS / FFT_POINTS; // Frequency step
const double Mag = 1.0; // Magnitude of the input signal
const int NP = (int)(1.0 / F / DT);

double Noise()
{
    double T = 0.0;
    for (int j = 0; j < 12; j++) 
        T += ((double)rand() / RAND_MAX);
    return (T - 6);
}

OPENFILENAMEA ofn;
HANDLE hFile;
fftw_complex* In, * Out;
fftw_plan pDir;
int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    double S[FFT_POINTS];
    double SNR_values[FFT_POINTS];
    char Txt[512];
    sprintf_s(Txt, "samples_noise.txt");
    memset(&ofn, 0, sizeof(OPENFILENAME));
    ofn.lStructSize = sizeof(OPENFILENAME);
    ofn.hwndOwner = NULL;
    ofn.lpstrFilter = "Data Files(*.dat)\0*.dat;\0Any Files(*.*)\0\*.*\0";
    ofn.lpstrFile = Txt;
    ofn.nFilterIndex = 1;
    ofn.nMaxFile = sizeof(Txt);
    ofn.lpstrTitle = "Open file";
    ofn.Flags = OFN_EXPLORER | OFN_OVERWRITEPROMPT;
    if (!GetSaveFileNameA(&ofn)) return FALSE;
    hFile = CreateFileA(ofn.lpstrFile, GENERIC_WRITE, FILE_SHARE_READ, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        MessageBoxW(NULL, L"File is not created", L"FFT testing", MB_OK);
        return FALSE;
    }

    In = (fftw_complex*)VirtualAlloc(NULL, FFT_POINTS * sizeof(fftw_complex), MEM_COMMIT,
        PAGE_READWRITE);
    Out = (fftw_complex*)VirtualAlloc(NULL, FFT_POINTS * sizeof(fftw_complex), MEM_COMMIT,
        PAGE_READWRITE);
    if ((In == NULL) || (Out == NULL))
    {
        MessageBoxW(NULL, L"Not enough memory", L"FFT testing", MB_OK);
        return FALSE;
    }
    pDir = fftw_plan_dft_1d(FFT_POINTS, In, Out, FFTW_FORWARD, FFTW_ESTIMATE);
    if (pDir == NULL)
    {
        MessageBoxW(NULL, L"FFTW plan was not created", L"FFT testing", MB_OK);
        return FALSE;
    }
    ZeroMemory(In, FFT_POINTS * sizeof(fftw_complex));

    ////sin
    ///*for (int i = 0; i < FFT_POINTS; i++)
    //{
    //  S[i] = Mag * cos(2 * M_PI * F * DT * i);
    //  In[i][0] = Mag * cos(2 * M_PI * F * DT * i);
    //}
    //*/

    //meandr
    //int NP = (int)(1.0 / F / DT);
    //for (int i = 0; i < FFT_POINTS; i++)
    //  if (i % NP < NP / 2)
    //    In[i][0] = S[i] = Mag;
    //  else
    //    In[i][0] = S[i] = -Mag;
    
    //unipolar
    /*for (int i = 0; i < FFT_POINTS; i++) {
        if (i % NP < NP * 0.25) {
            In[i][0] = Mag;
        }
        else {
            In[i][0] = 0;
        }
    }*/

    ////saw wrecked
    //for (int i = 0; i < FFT_POINTS; i++) {
    //  In[i][0] = S[i] = 2 * Mag * ((i % NP) / NP);
    //}

    // saw 
    //for (int i = 0; i < FFT_POINTS; i++) {
    //    In[i][0] = S[i] = 2 * Mag * ((i % NP) / (double)NP - 0.5); // around 0
    //}

    //dirac
    /*for (int i = 0; i < FFT_POINTS; i++) {
        In[i][0] = S[i] = Mag;
    }*/

    //dirac impulse
    /*int impulseWidth = 10;
    for (int i = 0; i < FFT_POINTS; ++i) {
        if (i >= 0 && i < impulseWidth) {
            In[i][0] = Mag;
        }
        else {
            In[i][0] = 0.0;
        }
    }*/

    //triangle
    /*for (int i = 0; i < FFT_POINTS; i++) {
      In[i][0] = S[i] = FFT_POINTS / 2 - abs(i - FFT_POINTS / 2);
    }*/

    //noise
    for (int i = 0; i < FFT_POINTS; i++) {
        //In[i][0] = S[i] = Mag * cos(2 * M_PI * F * DT * i);
        In[i][0] = S[i] = Noise();
    }

    fftw_execute(pDir);

    char buffer[256];
    DWORD ByteNum;
    double P, dB;

    /*for (int i = 0; i < FFT_POINTS; i++) {
        P = (Out[i][0] * Out[i][0] + Out[i][1] * Out[i][1]) / FFT_POINTS2;
        sprintf_s(buffer, "%.8g, %.8g\r\n",i * DF, S[i]);
        WriteFile(hFile, buffer, strlen(buffer), &ByteNum, NULL);
    }*/
    for (int i = 0; i < FFT_POINTS; i++)
    {
        P = (Out[i][0] * Out[i][0] + Out[i][1] * Out[i][1]) / FFT_POINTS2;
        //SNR_values[i] = 10 * log10((In[i][0] + Noise()) / Noise());
        //sprintf_s(buffer, "%.8g\t%.8g\t%.8g\t%.8g\r\n", i * DF, P, 10 * log10(P), SNR_values[i]);
        sprintf_s(buffer, "%.8g\t%.8g\t%.8g\r\n", i * DF, P, 10 * log10(P));
        WriteFile(hFile, buffer, strlen(buffer), &ByteNum, NULL);
    }


    //im re
    /*for (int i = 0; i < FFT_POINTS; i++) {
      P = (Out[i][0] * Out[i][0] + Out[i][1] * Out[i][1]) / FFT_POINTS2;
      sprintf_s(buffer, "%.8g,%.8g,%.8g,%.8g,%.8g,%.8g\r\n",i * DF, Out[i][0] / FFT_POINTS, Out[i][1] / FFT_POINTS, S[i], P, 10 * log10(P));
      WriteFile(hFile, buffer, strlen(buffer), &ByteNum, NULL);

    }*/


    MessageBoxA(NULL, "i'm done", "FFT testing", MB_OK);
    CloseHandle(hFile);
    VirtualFree(In, 0, MEM_RELEASE);
    VirtualFree(Out, 0, MEM_RELEASE);
    fftw_destroy_plan(pDir);
    return 0;
}
