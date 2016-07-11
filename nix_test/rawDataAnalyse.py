# Ajayrama Kumaraswamy, 2016
# Ginjang project, LMU

from neoNIXIO import tag2AnalogSignal, multiTag2SpikeTrain, property2qu
import nix
import os
import quantities as qu
from neo import SpikeTrain


def getSpikeTrainStartStop(tagType, tagMetadata, Fs):
    '''
    Internal function, don't use
    '''

    stimStart = property2qu(tagMetadata.props['StimulusStart'])[0]
    stimEnd = property2qu(tagMetadata.props['StimulusEnd'])[0]

    if tagType == 'DuringStimulus':

        tStart = stimStart
        tStop = stimEnd

    if tagType == 'BeforeStimulus':

        tStop = stimStart
        tStart = tStop - Fs

    if tagType == 'AfterStimulus':

        tStart = stimEnd
        tStop = tStart + Fs

    return tStart, tStop



class RawDataAnalyser(object):
    '''
    Class used to collect methods for accessing the processed electrophysiology data of our project
    '''

    def __init__(self, expName, dirpath):
        '''

        :param expName: string, experiment name/ID
        :param dirpath: string, path for finding the NIX files
        '''

        self.expName = expName
        self.nixFile = nix.File.open(os.path.join(dirpath, expName + '.h5'), nix.FileMode.ReadOnly)

    def getContResps(self, freqs=None, types=None):
        '''
        Collect and return the responses of the neuron from the current experiment to vibration stimulii of specified frequencies and types
        :param freqs: iterable of floats, the frequencies of vibration stimulii to which responses are collected
        :param types: string, must be one of 'BeforeStimulus', 'DuringStimulus' or 'AfterSimulus'. They stand for intervals of
        3 seconds before applying stimulus, during the stimulus and 3 seconds after the end of applying the stimulus.
        :return: resps, dict. resps has freqs as keys and freqResps as values. Each of the freqResps is a list of dicts,
        one dict per trial. Each of these dicts have types as keys and neo.analogsignal as values.
        '''

        if freqs is None:

            sec = self.nixFile.sections['VibrationStimulii-Raw'].sections['ContinuousStimulii']
            freqs = [v.value for v in sec.props['FrequenciesUsed'].values]

        if types is None:

            types = ['BeforeStimulus', 'DuringStimulus', 'AfterStimulus']

        resps = {}
        allFreqSecs = self.nixFile.sections['VibrationStimulii-Processed'].sections['ContinuousStimulii'].sections
        freqSecs = {}

        for fs in allFreqSecs:

            freq = fs.props['Frequency'].values[0].value
            if freq in freqs:
                freqSecs[freq] = fs


        for freq in freqs:

            if freq in freqSecs.viewkeys():
                resps[freq] = []
                nTrials = len(freqSecs[freq].sections)

                for ind in range(nTrials):

                    resps[freq].append({})

        freqSecs = freqSecs.values()


        for tag in self.nixFile.blocks['RawDataTraces'].tags:

            if tag.metadata.parent in freqSecs and tag.type in types:

                freq = tag.metadata.parent.props['Frequency'].values[0].value

                analogSignal = tag2AnalogSignal(tag, 1)

                resps[freq][int(tag.metadata.name[5:]) - 1][tag.type] = analogSignal

        return resps

    def getContSpikes(self, freqs=None, types=None):
        '''
        Collect and return the spikes of the neuron from the current experiment to vibration stimulii of specified frequencies and types
        :param freqs: iterable of floats, the frequencies of vibration stimulii to which responses are collected
        :param types: string, must be one of 'BeforeStimulus', 'DuringStimulus' or 'AfterSimulus'. They stand for intervals of
        3 seconds before applying stimulus, during the stimulus and 3 seconds after the end of applying the stimulus.
        :return: spikes, dict. spikes has freqs as keys and freqSpikes as values. Each of the freqSpikes is a list of dicts,
        one dict per trial. Each of these dicts have types as keys and neo.spiketrain as values.
        '''

        if freqs is None:

            sec = self.nixFile.sections['VibrationStimulii-Raw'].sections['ContinuousStimulii']
            freqs = [v.value for v in sec.props['FrequenciesUsed'].values]

        if types is None:

            types = ['BeforeStimulus', 'DuringStimulus', 'AfterStimulus']

        spikes = {}

        allFreqSecs = self.nixFile.sections['VibrationStimulii-Processed'].sections['ContinuousStimulii'].sections
        freqSecs = {}

        Fs = 3 * qu.s

        for fs in allFreqSecs:

            freq = fs.props['Frequency'].values[0].value
            if freq in freqs:
                freqSecs[freq] = fs
                spikes[freq] = []
                for sec in fs.sections:
                    temp = {}
                    for typ in types:

                        tStart, tStop = getSpikeTrainStartStop(typ, sec, Fs)
                        temp[typ] = SpikeTrain(times=[], t_start=tStart, t_stop=tStop, units=tStart.units)
                    spikes[freq].append(temp)


        freqSecs = freqSecs.values()

        for tag in self.nixFile.blocks['RawDataTraces'].multi_tags:

            if tag.metadata.parent in freqSecs and tag.type in types:

                freq = tag.metadata.parent.props['Frequency'].values[0].value

                tStart, tStop = getSpikeTrainStartStop(tag.type, tag.metadata, Fs)

                sp = multiTag2SpikeTrain(tag, tStart, tStop)

                spikes[freq][int(tag.metadata.name[5:]) - 1][tag.type] = sp



        return spikes
