# Ajayrama Kumaraswamy, 2016
# Ginjang Project, LMU

import nix
import neo
import quantities as qu
import numpy as np

qu2Val = lambda x: nix.Value(float(x))
quUnitStr = lambda x: x.dimensionality.string

#***********************************************************************************************************************

def addAnalogSignal2Block(blk, analogSignal):
    '''
    Create a new data array in the block blk and add the data in analogSignal to it
    :param blk: nix.block
    :param analogSignal: neo.analogsignal
    :return: data, nix.data_array, the newly added data_array
    '''

    assert hasattr(analogSignal, 'name'), 'Analog signal has no name'

    data = blk.create_data_array(analogSignal.name, 'nix.regular_sampled', data=analogSignal.magnitude)

    data.unit = quUnitStr(analogSignal)
    data.label = analogSignal.name

    qu.set_default_units = 'SI'
    samplingPeriod = analogSignal.sampling_period.simplified
    t = data.append_sampled_dimension(float(samplingPeriod))
    t.label = 'time'
    t.unit = quUnitStr(samplingPeriod)
    t.offset = float(analogSignal.t_start.simplified)

    return data

#***********************************************************************************************************************

def dataArray2AnalogSignal(dataArray):
    '''
    Convert a nix data_array into a neo analogsignal
    :param dataArray: nix.data_array
    :return: neo.analogsignal
    '''

    for dim in dataArray.dimensions:

        if isinstance(dim, nix.SampledDimension):

            t_start = qu.Quantity(dim.offset, units=dim.unit)
            samplingPeriod = qu.Quantity(dim.sampling_interval, units=dim.unit)

            break


    analogSignal = neo.AnalogSignal(signal=dataArray[:],
                                    units=dataArray.unit,
                                    sampling_period=samplingPeriod,
                                    t_start=t_start)

    analogSignal.name = dataArray.name

    return analogSignal

#***********************************************************************************************************************

def property2qu(property):
    '''
    Convert a nix property to a quantities Quantity
    :param property: nix.property
    :return: quantities.Quantity
    '''

    return qu.Quantity([v.value for v in property.values], units=property.unit)

#***********************************************************************************************************************

def addQuantity2section(sec, quant, name):
    '''
    Create new property in section sec and add the data in quantity.Quantitiy quant to it
    :param sec: nix.section
    :param quant: quantities.Quantity
    :param name: name of the property to add
    :return: p, nix.property, the property added.
    '''

    if quant.shape == ():

        p = sec.create_property(name, [qu2Val(quant)])

    #only 1D arrays
    elif len(quant.shape) == 1:

        #not an empty 1D array
        if quant.shape[0]:

            p = sec.create_property(name, [qu2Val(x) for x in quant])

        else:
            raise(ValueError('Quantity passed must be either scalar or 1 dimensional'))

    else:
            raise(ValueError('Quantity passed must be either scalar or 1 dimensional'))

    p.unit = quUnitStr(quant)

    return p

#***********************************************************************************************************************

def createPosDA(name, pos, blk):
    '''
    Create a data_array of type 'nix.positions' with the pos data in the block blk
    :param name: string, name of the data_array to create
    :param pos: iterable of floats, data to be added to the created data_array
    :param blk: nix.block, the block in which the data_array is to be created
    :return: positions, nix.data_array, the newly created data_array
    '''

    positions = blk.create_data_array(name, 'nix.positions', data=pos)
    positions.append_set_dimension()
    positions.append_set_dimension()

    return positions

#***********************************************************************************************************************

def createExtDA(name, ext, blk):
    '''
   Create a data_array of type 'nix.extents' with the pos data in the block blk
   :param name: string, name of the data_array to create
   :param ext: iterable of floats, data to be added to the created data_array
   :param blk: nix.block, the block in which the data_array is to be created
   :return: extents, nix.data_array, the newly created data_array
   '''

    extents = blk.create_data_array(name, 'nix.extents', data=ext)
    extents.append_set_dimension()
    extents.append_set_dimension()

    return extents

#***********************************************************************************************************************

def tag2AnalogSignal(tag, refInd):
    '''
    Create a neo.analogsignal from the snippet of data represented by a nix.tag and its reference at index refInd
    :param tag: nix.tag
    :param refInd: the index of the reference among those of the tag to use
    :return: neo.analogsignal with the snipped of reference data tagged by tag.
    '''

    ref = tag.references[refInd]
    dim = ref.dimensions[0]
    offset = dim.offset
    ts = dim.sampling_interval
    nSamples = ref[:].shape[0]

    startInd = max(0, int(np.floor((tag.position[0] - offset) / ts)))
    endInd = min(startInd + int(np.floor(tag.extent[0] / ts)) + 1, nSamples)
    trace = ref[startInd:endInd]

    analogSignal = neo.AnalogSignal(signal=trace,
                                    units=ref.unit,
                                    sampling_period=qu.Quantity(ts, units=dim.unit),
                                    t_start=qu.Quantity(offset + startInd * ts, units=dim.unit))

    # trace = tag.retrieve_data(refInd)[:]
    # tVec = tag.position[0] + np.linspace(0, tag.extent[0], trace.shape[0])

    return analogSignal

#***********************************************************************************************************************

def multiTag2SpikeTrain(tag, tStart, tStop):
    '''
    Create a neo.spiketrain from nix.multitag
    :param tag: nix.multitag
    :param tStart: float, time of start of the spike train in units of the multitag
    :param tStop: float, time of stop of the spike train in units of the multitag
    :return: neo.spiketrain
    '''

    sp = neo.SpikeTrain(times=tag.positions[:], t_start=tStart, t_stop=tStop, units=tag.units[0])

    return sp


#***********************************************************************************************************************

def sliceAnalogSignal(analogSignal, sliceStartTime=None, sliceEndTime=None):
    '''
    Slice a neo.analogsignal using times instead of indices
    :param analogSignal: neo.analogsignal
    :param sliceStartTime: quantities.Quantity, start time of the slice, must be at least analogSignal.t_start.
    If it is None, slice starts at the beginning of analogSignal
    :param sliceEndTime: quantities.Quantity, stop time of the slice, must be at most analogSignal.t_start
    If it is None, slice ends at the end of analogSignal
    :return: neo.analogsignal, the slice of analogSignal between sliceStartTime and sliceEndTime.
    '''

    assert type(analogSignal) is neo.AnalogSignal, 'analogSignal must be a neo.AnalogSignal'

    if sliceStartTime is None:
        sliceStartTime = analogSignal.t_start

    if sliceEndTime is None:
        sliceEndTime = analogSignal.t_stop

    assert type(sliceStartTime) is qu.Quantity, 'sliceStartTime must be a quantities.Quanitity'
    assert type(sliceEndTime) is qu.Quantity, 'sliceEndTime must be a quantities.Quanitity'

    assert sliceStartTime >= analogSignal.t_start, 'sliceStartTime must be >= analogSignal.t_start'
    assert sliceEndTime <= analogSignal.t_stop, 'sliceEndTime must be <= analogSignal.t_stop'

    sliceStartInd = int(((sliceStartTime - analogSignal.t_start) / analogSignal.sampling_period).simplified)
    sliceEndInd = int(((sliceEndTime - analogSignal.t_start) / analogSignal.sampling_period).simplified)

    return analogSignal[sliceStartInd: sliceEndInd + 1]

#***********************************************************************************************************************
