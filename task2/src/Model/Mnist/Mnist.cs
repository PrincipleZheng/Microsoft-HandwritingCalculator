using Microsoft.ML.Scoring;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;

namespace Model
{
    public partial class Mnist
    {
        const string modelName = "Mnist";
        private ModelManager manager;

        private static List<string> inferInputNames = new List<string> { "inputs" };
        private static List<string> inferOutputNames = new List<string> { "outputs" };

        /// <summary>
        /// Returns an instance of Mnist model.
        /// </summary>
        public Mnist()
        {
            string codeBase = Assembly.GetExecutingAssembly().CodeBase;
            UriBuilder uri = new UriBuilder(codeBase);
            string dllpath = Uri.UnescapeDataString(uri.Path);
            string modelpath = Path.Combine(Path.GetDirectoryName(dllpath), "Mnist");
            string path = Path.Combine(modelpath, "00000001");
            manager = new ModelManager(path, true);
            manager.InitModel(modelName, int.MaxValue);
        }

        /// <summary>
        /// Returns instance of Mnist model instantiated from exported model path.
        /// </summary>
        /// <param name="path">Exported model directory.</param>
        public Mnist(string path)
        {
            manager = new ModelManager(path, true);
            manager.InitModel(modelName, int.MaxValue);
        }

        /// <summary>
        /// Runs inference on Mnist model for a batch of inputs.
        /// The shape of each input is the same as that for the non-batch case above.
        /// </summary>
        public IEnumerable<IEnumerable<long>> Infer(IEnumerable<IEnumerable<float>> inputsBatch)
        {
            List<float> inputsCombined = new List<float>();
            long batchCount = 0;
            foreach (var input in inputsBatch)
            {
                inputsCombined.AddRange(input);
                ++batchCount;
            }

            List<Tensor> result = manager.RunModel(
                modelName,
                int.MaxValue,
                inferInputNames,
                new List<Tensor> { new Tensor(inputsCombined, new List<long> { batchCount, 28, 28, 1 }) },
                inferOutputNames
            );

            int outputsBatchNum = (int)result[0].GetShape()[0];
            int outputsBatchSize = (int)result[0].GetShape().Aggregate((a, x) => a * x) / outputsBatchNum;
            for (int batchNum = 0, offset = 0; batchNum < outputsBatchNum; batchNum++, offset += outputsBatchSize)
            {
                List<long> tmp = new List<long>();
                result[0].CopyTo(tmp, offset, outputsBatchSize);
                yield return tmp;
            }
        }

//Infer函数的返回值类型在python里无法被正常接收和使用,无奈选择传回模型类中处理好再返回String类型结果
//注：后来和同学交流了解到是pythonnet的版本问题，更新为3.0.0a1即可
        public String Getoutput(IEnumerable<IEnumerable<long>> input)
        {
            return input.First().First().ToString();
        }

        public IEnumerable<IEnumerable<long>> Infer2(IEnumerable<IEnumerable<float>> inputsBatch)
        {
            var ret = new List<long>(12);
            ret.Add(123);
            return new List<IEnumerable<long>> { ret };
        }
    } // END OF CLASS
} // END OF NAMESPACE
