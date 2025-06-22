package com.encryption.utils;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class PerformanceMetrics {
    public static void plotPerformanceMetrics(
            List<Double> encryptTimes,
            List<Double> decryptTimes,
            List<Double> encryptMemory,
            List<Double> decryptMemory,
            List<Integer> inputSizes) throws IOException {
        
        // Create time performance chart
        XYSeries encryptTimeSeries = new XYSeries("Encryption Time");
        XYSeries decryptTimeSeries = new XYSeries("Decryption Time");
        
        for (int i = 0; i < inputSizes.size(); i++) {
            encryptTimeSeries.add(inputSizes.get(i), encryptTimes.get(i));
            decryptTimeSeries.add(inputSizes.get(i), decryptTimes.get(i));
        }
        
        XYSeriesCollection timeDataset = new XYSeriesCollection();
        timeDataset.addSeries(encryptTimeSeries);
        timeDataset.addSeries(decryptTimeSeries);
        
        JFreeChart timeChart = ChartFactory.createXYLineChart(
            "Encryption/Decryption Time vs Input Size",
            "Input Size (bytes)",
            "Time (seconds)",
            timeDataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        );
        
        // Create memory performance chart
        XYSeries encryptMemorySeries = new XYSeries("Encryption Memory");
        XYSeries decryptMemorySeries = new XYSeries("Decryption Memory");
        
        for (int i = 0; i < inputSizes.size(); i++) {
            encryptMemorySeries.add(inputSizes.get(i), encryptMemory.get(i));
            decryptMemorySeries.add(inputSizes.get(i), decryptMemory.get(i));
        }
        
        XYSeriesCollection memoryDataset = new XYSeriesCollection();
        memoryDataset.addSeries(encryptMemorySeries);
        memoryDataset.addSeries(decryptMemorySeries);
        
        JFreeChart memoryChart = ChartFactory.createXYLineChart(
            "Encryption/Decryption Memory Usage vs Input Size",
            "Input Size (bytes)",
            "Memory Usage (KB)",
            memoryDataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        );
        
        // Save charts
        ChartUtils.saveChartAsPNG(new File("performance_time.png"), timeChart, 800, 600);
        ChartUtils.saveChartAsPNG(new File("performance_memory.png"), memoryChart, 800, 600);
    }
} 